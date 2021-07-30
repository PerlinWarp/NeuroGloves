from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread

import myo
import numpy as np

import serial

MYO_PATH = "./myo-sdk-win-0.9.0/"

def pack_vals(arr):
		# arr should be of length 13
		return b"%d&%d&%d&%d&%d&%d&%d&%d&%d&%d&%d&%d&%d\n" % tuple(arr)

class EmgCollector(myo.DeviceListener):
	"""
	Collects EMG data in a queue with *n* maximum number of elements.
	"""

	def __init__(self, n):
		self.n = n
		self.lock = Lock()
		self.emg_data_queue = deque(maxlen=n)
		self.last_emg = [0]*8

	def get_emg_data(self):
		with self.lock:
			return list(self.emg_data_queue)

	# myo.DeviceListener

	def on_connected(self, event):
		event.device.stream_emg(True)

	def on_emg(self, event):
		with self.lock:
			self.emg_data_queue.append((event.timestamp, event.emg))
			self.last_emg = event.emg

class toSerial(object):

	def __init__(self, listener):
		# Myo Setup
		self.n = listener.n
		self.listener = listener
		
		# Serial Setup
		self.ser = serial.Serial('COM6','115200')  # open serial port
		print("Writing to", self.ser.name)         # check which port was really used
		self.ser.write(b'hello\n')     # write a string

	def emg_to_fingers(self):
		emg_data = self.listener.last_emg
		emg_data = np.array(emg_data)
		print("EMG DATA", emg_data)
		# Rectify: [-128, 127] -> [0,256]
		emg_data = np.abs(emg_data)
		# Scale
		emg_data = (emg_data/80 * 1024)/8
		return sum(emg_data)

	def main(self):
		while True:
				try:
						e = self.emg_to_fingers()
						e = int(e)
						
							
						emg_d = self.listener.get_emg_data()
						emg_d = abs(np.array([x[1] for x in emg_d]).T)
						e = int( (np.sum(emg_d) / 3000) * 1024)
						print("SUM", e)

						if e:
							vals = pack_vals([e]*13)
							print("VALS", e)
							self.ser.write(vals)

				except KeyboardInterrupt:
						print("Ending...")
						self.ser.close()             # close port
						quit()


def main():
	try:
		myo.init(sdk_path=MYO_PATH)
		hub = myo.Hub()
		listener = EmgCollector(50)
		with hub.run_in_background(listener.on_event):
			toSerial(listener).main()
	except KeyboardInterrupt:
		print("Quitting...")
		quit()


if __name__ == '__main__':
	main()