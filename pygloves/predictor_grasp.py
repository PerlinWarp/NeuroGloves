import multiprocessing
import numpy as np

from pyomyo import Myo, emg_mode
from pygloves_utils import serial_utils as s

# ------------ Myo Setup ---------------
def myo_worker(q):
	m = Myo(mode=emg_mode.PREPROCESSED)
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

class Predictor:
	def __init__(self):
		self.grasp = False
		self.last_grasp = False
		self.last_val = 0

	def predict(self, emg_data):
		'''
		return [0,1,2,3,4]
		'''
		emg_data = np.array(emg_data).reshape(1,8)

		# Rectify: [-128, 127] -> [0,256]
		emg_data = np.abs(emg_data)
		# Scale the input
		s = np.sum(emg_data)
		s = int((s/3000)*100)/100
		print("SUM", s)
		
		# Make a prediction from s
		pred = [s]*5

		# Update last grasp
		print(self.grasp, self.last_grasp)
		self.last_grasp = self.grasp
		return pred

if __name__ == '__main__':
	# IPS Setup
	ipc = s.ipc.NamedPipe()

	q = multiprocessing.Queue()
	p = multiprocessing.Process(target=myo_worker, args=(q,))
	p.start()
	predictor = Predictor()
	while True:
		try:
			while not q.empty():
				emg = list(q.get())
				print("EMG:", emg)
				fingers = predictor.predict(emg)

				if (fingers is not None) and (fingers is not predictor.last_val):
					print("Fingers", fingers)
					ipc.send(fingers)
					predictor.last_val = fingers

		except KeyboardInterrupt:
				print("Ending...")
				quit()