import multiprocessing
import serial

from collections import deque
from threading import Lock, Thread

from pyomyo import Myo, emg_mode
import serial_utils as s

# Arguments
COM_PORT = "COM9"
FILE_NAME = "myo_raw_glove2" + ".csv"
MODE = emg_mode.PREPROCESSED

# Serial Setup

def serial_worker(port, sarr):
	ser = serial.Serial(port,'115200', timeout=1)  # open serial port
	print("Listening on "+port)

	while True:
		try:
		    read = ser.readline()
		    fingers = s.decode_alpha_serial(read)
		    if fingers is not None:
		    	# Update the shared array
		    	for i in range(0,5):
		    		sarr[i] =  fingers[i]
		    else:
		    	print("None")
		except KeyboardInterrupt:
			print("Breaking...")
			ser.close()
			quit()

# Myo Setup
# ------------ Myo Setup ---------------

def myo_worker(q, emg_mode):
	m = Myo(mode=emg_mode)
	m.connect()
	
	def add_to_queue(emg, movement):
		q.put(emg)

	m.add_emg_handler(add_to_queue)
	
	def print_battery(bat):
		print("Battery level:", bat)

	m.add_battery_handler(print_battery)

	# Orange logo and bar LEDs
	m.set_leds([128, 128, 0], [128, 128, 0])
	# Vibrate to know we connected okay
	m.vibrate(1)
	
	"""worker function"""
	while True:
		try:
			m.run()
		except KeyboardInterrupt:
			m.set_leds([128, 128, 255], [128, 128, 255])
			m.vibrate(1)
			m.disconnect()
	print("Worker Stopped")

if __name__ == '__main__':
	# Serial Reader Process
	arr = multiprocessing.Array('i', range(5))
	s = multiprocessing.Process(target=serial_worker, args=(COM_PORT, arr,))
	# Myo Process
	q = multiprocessing.Queue()
	p = multiprocessing.Process(target=myo_worker, args=(q,MODE,))
	p.start()
	s.start()

	myo_data = []
	glove_data = []
	glove = [0,1,2,3,4]
	print("Waiting..")
	try:
		while True:	
			# Wait for Serial to work
			while glove == [0,1,2,3,4]:
				glove = list(arr)

			while not q.empty():
				emg = list(q.get())
				glove = list(arr)
				print("Myo: ",emg)
				print("Serial", list(arr))
				myo_data.append(emg)
				glove_data.append(glove)

	except KeyboardInterrupt:
		print("Saving data")
		print("Glove data",len(myo_data))
		print("EMG data",len(glove_data))
		import pandas as pd
		finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
		myo_cols = ["Channel_1", "Channel_2", "Channel_3", "Channel_4", "Channel_5", "Channel_6", "Channel_7", "Channel_8"]

		# Put in dfs
		myo_df = pd.DataFrame(myo_data, columns=myo_cols)
		glove_df = pd.DataFrame(glove_data, columns=finger_names)
		# Combine them
		df = myo_df.join(glove_df)
		df.to_csv(FILE_NAME, index=False)
		print("CSV Saved", FILE_NAME)
		
		print("Quitting")
		p.kill()
		s.kill()
		quit()