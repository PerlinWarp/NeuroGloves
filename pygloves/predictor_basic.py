'''
Uses the finger classifier to predict which finger is closed
Then sends the data to COMPORT
This can be visualised using OpenGloves or pygloves_utils/lerp_finger_from_serial.py
'''

from collections import Counter, deque
import struct
import sys
import time

import serial
import pygame
from pygame.locals import *
import numpy as np
from xgboost import XGBClassifier

from pyomyo import Myo, emg_mode
from pyomyo.Classifier import Live_Classifier, MyoClassifier, EMGHandler
from pygloves_utils import serial_utils as s

'''
A bodge of a predictor
Uses class 0 as resting 
1 - Thumb curl
...
5 - Pinky curl
6 - Grab
7 - Pinch
'''
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

class SVM_Classifier(Live_Classifier):
	'''
	Live implimentation of an SVM Classifier
	'''
	def __init__(self):
		Live_Classifier.__init__(self, None, "SVM", (100,0,100))

	def train(self, X, Y):
		self.X = X
		self.Y = Y
		try:
			if self.X.shape[0] > 0: 
				clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
				#clf = make_pipeline(StandardScaler(), SVC(kernel="linear", C=0.025))

				clf.fit(self.X, self.Y)
				self.model = clf
		except:
			# SVM Errors when we only have data for 1 class.
			self.model = None

	def classify(self, emg):
		if self.X.shape[0] == 0 or self.model == None:
			# We have no data or model, return 0
			return 0

		x = np.array(emg).reshape(1,-1)
		pred = self.model.predict(x)
		return int(pred[0])


if __name__ == '__main__':
	# Serial Setup
	ser = serial.Serial('COM6','115200')  # open serial port
	ser.flushInput()
	print("Writing to", ser.name, "\nWaiting for consumer")         # check which port was really used

	pygame.init()
	w, h = 800, 320
	scr = pygame.display.set_mode((w, h))
	font = pygame.font.Font(None, 30)

	# Make an ML Model to train and test with live
	# XGBoost Classifier Example
	# model = XGBClassifier(eval_metric='logloss')
	# clr = Live_Classifier(model, name="XG", color=(50,50,255))
	# m = MyoClassifier(clr, mode=emg_mode.PREPROCESSED)

	m = MyoClassifier(SVM_Classifier(), mode=emg_mode.PREPROCESSED, hist_len=12)

	hnd = EMGHandler(m)
	m.add_emg_handler(hnd)
	m.connect()

	# Set Myo LED color to model color
	m.set_leds(m.cls.color, m.cls.color)
	# Set pygame window name
	pygame.display.set_caption(m.cls.name)

	try:
		while True:
			# Run the Myo, get more data
			m.run()
			# Run the classifier GUI
			m.run_gui(hnd, scr, font, w, h)	

			r = m.history_cnt.most_common(1)[0][0]
			print(f"Class {r}, \"Confidence\", {m.history_cnt[r]/m.hist_len}")
			fingers = [0,0,0,0,0]
			f = int(r)
			scaled_conf = int(1023 * m.history_cnt[r]/m.hist_len)
			if f == 0:
				pass
			elif (f == 6): # Grab
				fingers = [scaled_conf] * 5
				# TODO also send grab value to steam
			else:
				# We have predicted a finger
				fingers[f-1] = scaled_conf
			vals = s.encode_alpha_serial(fingers)
			print("Fingers", fingers, vals)
			ser.write(vals)

	except KeyboardInterrupt:
		m.disconnect()
		print()
		pygame.quit()
		ser.flushInput()
		ser.close()
	finally:
		m.disconnect()
		print()
		pygame.quit()
		ser.flushInput()
		ser.close()
