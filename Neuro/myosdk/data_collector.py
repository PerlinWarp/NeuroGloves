import multiprocessing
import serial

from collections import deque
from threading import Lock, Thread

import myo

# Arguments
COM_PORT = "COM8"
MYO_PATH = "./myo-sdk-win-0.9.0/"
FILE_NAME = "combined" + ".csv"

# Serial Setup
def decode_serial(s):
	if s == b'':
		return None
	else:
		# Decode the byte string to list of ints
		s = s.decode().rstrip().split('&')
		# Get rid of all other data than fingers
		s = s[0:5]
		# Cast to ints
		s = [int(f) for f in s]
		return s

def serial_worker(port, sarr):
	ser = serial.Serial(port,'115200', timeout=1)  # open serial port
	print("Listening on "+port)

	while True:
		try:
		    read = ser.readline()
		    fingers = decode_serial(read)
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

class EmgCollector(myo.DeviceListener):
	"""
	Collects EMG data in a queue with *n* maximum number of elements.
	"""

	def __init__(self, n, sarr):
		self.n = n
		self.lock = Lock()
		self.emg_data_queue = deque(maxlen=n)
		self.last_emg = [0]*8

		# Glove label array
		self.label = sarr
		self.emgs = []
		self.labels = []

	def get_emg_data(self):
		with self.lock:
			return list(self.emg_data_queue)

	# myo.DeviceListener

	def on_connected(self, event):
		print("Connected")
		event.device.stream_emg(True)

	def on_emg(self, event):
		with self.lock:
			self.emg_data_queue.append((event.timestamp, event.emg))
			self.last_emg = event.emg
			print("Last Serial", list(self.label), event.emg)

			label = list(self.label)
			# Add data
			self.labels.append(label)
			self.emgs.append(event.emg)

if __name__ == '__main__':
	arr = multiprocessing.Array('i', range(5))
	p = multiprocessing.Process(target=serial_worker, args=(COM_PORT, arr,))
	p.start()

	try:
		# Myo Setup
		myo.init(sdk_path=MYO_PATH)
		hub = myo.Hub()
		listener = EmgCollector(50, arr)
		with hub.run_in_background(listener.on_event):
			while True:
				pass

	except KeyboardInterrupt:
		print("Saving data")
		print("Glove data",len(listener.labels))
		print("EMG data",len(listener.emgs))
		import pandas as pd
		finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
		myo_cols = ["Channel_1", "Channel_2", "Channel_3", "Channel_4", "Channel_5", "Channel_6", "Channel_7", "Channel_8"]

		myo_data = listener.emgs
		glove_data = listener.labels
		# Put in dfs
		myo_df = pd.DataFrame(myo_data, columns=myo_cols)
		glove_df = pd.DataFrame(glove_data, columns=finger_names)
		# Combine them
		df = myo_df.join(glove_df)
		df.to_csv(FILE_NAME, index=False)
		print("CSV Saved", FILE_NAME)
		
		print("Quitting")
		p.kill()
		quit()