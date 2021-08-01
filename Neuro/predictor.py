import multiprocessing
from myo_serial import MyoRaw
import numpy as np

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from keras.models import load_model
import joblib

import serial

def pack_vals(arr):
		# arr should be of length 13
		return b"%d&%d&%d&%d&%d&0&0&0&0&0&0&0&0\n" % tuple(arr)

# ------------ Myo Setup ---------------
def myo_worker(q):
	m = MyoRaw(raw=False, filtered=True)
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


def predict(emg_data):
	emg_data = np.array(emg_data).reshape(1,8)

	# Rectify: [-128, 127] -> [0,256]
	emg_data = np.abs(emg_data)
	# Scale the input
	scaled_input = input_scaler.transform(emg_data)
	
	# Get a prediction
	pred = model.predict(scaled_input)
	# Scale it back to a value
	scaled_pred = output_scaler.inverse_transform(pred)
	scaled_pred = scaled_pred[0].astype(int)
	pred = list(scaled_pred)
	return pred

if __name__ == '__main__':
	# Serial Setup
	ser = serial.Serial('COM6','115200')  # open serial port
	print("Writing to", ser.name)         # check which port was really used
	ser.write(b'hello\n')     # write a string

	# Model Setup
	# Load the Keras model
	model_name = "NNBasic"
	model = load_model(f"../models/{model_name}.h5")

	input_scaler = joblib.load(f'../models/{model_name}-EMG.gz')
	output_scaler = joblib.load(f'../models/{model_name}-Hand.gz')

	q = multiprocessing.Queue()
	p = multiprocessing.Process(target=myo_worker, args=(q,))
	p.start()

	while True:
		try:
			while not q.empty():
				emg = list(q.get())
				print("EMG:", emg)
				e = predict(emg)

				if e is not None:
					vals = pack_vals(e)
					print("Vals: {:03d},{:03d},{:03d},{:03d},{:03d}".format(e[0],e[1],e[2],e[3],e[4]))
					ser.write(vals)

		except KeyboardInterrupt:
				print("Ending...")
				ser.close()             # close port
				#p.kill()
				quit()
