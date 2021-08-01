from collections import Counter, deque
import struct
import sys
import time

import serial
import pygame
from pygame.locals import *
import numpy as np

from myo_serial import MyoRaw

'''
A bodge of a predictor
Uses class 0 as resting 
1 - Thumb curl
...
5 - Pinky curl
6 - Grasp
7 - Point
'''

SUBSAMPLE = 3
K = 15

def pack_vals(arr):
		# arr should be of length 13
		'''
		0 - 4 - flexion
		...
		12 - grab 0/1
		13 - pinch 0/1
		'''
		return b"%d&%d&%d&%d&%d&0&0&0&0&0&0&%d&%d\n" % tuple(arr)

class Classifier(object):
	'''A wrapper for nearest-neighbor classifier that stores
	training data in vals0, ..., vals9.dat.'''

	def __init__(self):
		for i in range(10):
			with open('data/vals%d.dat' % i, 'ab') as f: pass
		self.read_data()

	def store_data(self, cls, vals):
		with open('data/vals%d.dat' % cls, 'ab') as f:
			f.write(pack('8H', *vals))

		self.train(np.vstack([self.X, vals]), np.hstack([self.Y, [cls]]))

	def read_data(self):
		X = []
		Y = []
		for i in range(10):
			X.append(np.fromfile('data/vals%d.dat' % i, dtype=np.uint16).reshape((-1, 8)))
			Y.append(i + np.zeros(X[-1].shape[0]))

		self.train(np.vstack(X), np.hstack(Y))

	def train(self, X, Y):
		self.X = X
		self.Y = Y
		self.nn = None

	def nearest(self, d):
		dists = ((self.X - d)**2).sum(1)
		ind = dists.argmin()
		return self.Y[ind]

	def classify(self, d):
		if self.X.shape[0] < K * SUBSAMPLE: return 0
		return self.nearest(d)


class Myo(MyoRaw):
	'''Adds higher-level pose classification and handling onto MyoRaw.'''

	HIST_LEN = 25

	def __init__(self, cls, tty=None):
		MyoRaw.__init__(self, tty, raw = False, filtered=True)
		self.cls = cls

		self.history = deque([0] * Myo.HIST_LEN, Myo.HIST_LEN)
		self.history_cnt = Counter(self.history)
		self.add_emg_handler(self.emg_handler)
		self.last_pose = None

		self.pose_handlers = []

	def emg_handler(self, emg, moving):
		y = self.cls.classify(emg)
		self.history_cnt[self.history[0]] -= 1
		self.history_cnt[y] += 1
		self.history.append(y)

		r, n = self.history_cnt.most_common(1)[0]
		if self.last_pose is None or (n > self.history_cnt[self.last_pose] + 5 and n > Myo.HIST_LEN / 2):
			self.on_raw_pose(r)
			self.last_pose = r

	def add_raw_pose_handler(self, h):
		self.pose_handlers.append(h)

	def on_raw_pose(self, pose):
		for h in self.pose_handlers:
			h(pose)

def pack(fmt, *args):
	return struct.pack('<' + fmt, *args)

def unpack(fmt, *args):
	return struct.unpack('<' + fmt, *args)

def text(scr, font, txt, pos, clr=(255,255,255)):
	scr.blit(font.render(txt, True, clr), pos)


class EMGHandler(object):
	def __init__(self, m):
		self.recording = -1
		self.m = m
		self.emg = (0,) * 8

	def __call__(self, emg, moving):
		self.emg = emg
		if self.recording >= 0:
			self.m.cls.store_data(self.recording, emg)

if __name__ == '__main__':
	# Serial Setup
	ser = serial.Serial('COM6','115200')  # open serial port
	print("Writing to", ser.name, "\nWaiting for consumer")         # check which port was really used

	pygame.init()
	w, h = 800, 320
	scr = pygame.display.set_mode((w, h))
	font = pygame.font.Font(None, 30)

	m = Myo(Classifier())
	hnd = EMGHandler(m)
	m.add_emg_handler(hnd)
	m.connect()

	m.add_raw_pose_handler(print)

	try:
		while True:
			m.run()

			r = m.history_cnt.most_common(1)[0][0]

			for ev in pygame.event.get():
				if ev.type == QUIT or (ev.type == KEYDOWN and ev.unicode == 'q'):
					raise KeyboardInterrupt()
				elif ev.type == KEYDOWN:
					if K_0 <= ev.key <= K_9:
						hnd.recording = ev.key - K_0
					elif K_KP0 <= ev.key <= K_KP9:
						hnd.recording = ev.key - K_Kp0
					elif ev.unicode == 'r':
						hnd.cl.read_data()
				elif ev.type == KEYUP:
					if K_0 <= ev.key <= K_9 or K_KP0 <= ev.key <= K_KP9:
						hnd.recording = -1

			scr.fill((0, 0, 0), (0, 0, w, h))

			for i in range(10):
				x = 0
				y = 0 + 30 * i

				clr = (0,200,0) if i == r else (255,255,255)

				txt = font.render('%5d' % (m.cls.Y == i).sum(), True, (255,255,255))
				scr.blit(txt, (x + 20, y))

				txt = font.render('%d' % i, True, clr)
				scr.blit(txt, (x + 110, y))


				scr.fill((0,0,0), (x+130, y + txt.get_height() / 2 - 10, len(m.history) * 20, 20))
				scr.fill(clr, (x+130, y + txt.get_height() / 2 - 10, m.history_cnt[i] * 20, 20))


			print(f"Class {r}, \"Confidence\", {m.history_cnt[r]/m.HIST_LEN}")
			fingers = [0,0,0,0,0,0,0]
			f = int(r)
			if f == 0:
				pass
			elif f == 6:
				# Activate grab
				fingers[5] = 1
			elif f == 7:
				# Activate Pinch
				fingers[6] = 1
			else:
				# We have predicted a finger
				fingers[f+1] = int(1023 * m.history_cnt[r]/m.HIST_LEN)
			vals = pack_vals(fingers)
			print(vals)
			ser.write(vals)
			pygame.display.flip()

	except KeyboardInterrupt:
		m.disconnect()
		print()
		pygame.quit()
		ser.close()
	finally:
		m.disconnect()
		print()
		pygame.quit()
		ser.close()
