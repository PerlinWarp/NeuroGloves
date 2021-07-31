from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread

import myo
import numpy as np

from keras.models import load_model
import joblib

import serial

MYO_PATH = "./myo-sdk-win-0.9.0/"

def pack_vals(arr):
		# arr should be of length 13
		return b"%d&%d&%d&%d&%d&0&0&0&0&0&0&0&0\n" % tuple(arr)

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

class predictor(object):

	def __init__(self, listener):
		# Myo Setup
		self.n = listener.n
		self.listener = listener
		
		# Serial Setup
		self.ser = serial.Serial('COM6','115200')  # open serial port
		print("Writing to", self.ser.name)         # check which port was really used
		self.ser.write(b'hello\n')     # write a string

		# Model Setup
		# Load the Keras model
		model_name = "NNRel-60secs-FULL-StanScaled"
		self.model = load_model(f"../../models/{model_name}.h5")

		self.input_scaler = joblib.load(f'../../models/{model_name}-EMG.gz')
		self.output_scaler = joblib.load(f'../../models/{model_name}-Hand.gz')

	def predict(self):
		emg_data = self.listener.last_emg
		emg_data = np.array(emg_data).reshape(1,8)
		print("EMG DATA", emg_data)

		# Rectify: [-128, 127] -> [0,256]
		emg_data = np.abs(emg_data)
		# Scale the input
		scaled_input = self.input_scaler.transform(emg_data)
		
		# Get a prediction
		pred = self.model.predict(scaled_input)
		# Scale it back to a value
		scaled_pred = self.output_scaler.inverse_transform(pred)
		scaled_pred = scaled_pred[0].astype(int)
		pred = list(scaled_pred)
		return pred

	def main(self):
		while True:
				try:
						e = self.predict()
						print("Pred:", e)

						if e is not None:
							vals = pack_vals(e)
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
			predictor(listener).main()
	except KeyboardInterrupt:
		print("Quitting...")
		quit()


if __name__ == '__main__':
	main()