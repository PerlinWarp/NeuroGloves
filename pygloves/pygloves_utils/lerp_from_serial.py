import multiprocessing
import re
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import bone
import serial_utils as s

# Use device manager to find the Arduino's serial port.
COM_PORT = "COM9"
RESET_SCALE = True
LEGACY_DECODE = False # If false, will use alpha encodings

q = multiprocessing.Queue()
# Plot Setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

# ------------ Serial Setup ---------------
def serial_worker(q):
	# Open Serial Port
	COM_PORT = "COM9"
	ser = serial.Serial(COM_PORT,'115200', timeout=1)  # open serial port
	print("Listening on "+COM_PORT)

	while True:
		try:
			# Read from serial
			read = ser.readline()
			if LEGACY_DECODE:
				fingers = s.decode_legacy_serial(read)
			else:
				fingers = s.decode_alpha_serial(read)
			# Add the decoded values to the queue
			q.put(fingers)
		except KeyboardInterrupt:
			print("Quitting thread...")
			ser.close()
			quit()

def animate(i):
	fingers = [0,0,0,0,0]
	while not(q.empty()):
		fingers = list(q.get())

	# Turn finger values into Lerp Vals
	val = fingers[0] / 1000
	print("Finger val", val)

	# Plot
	ax.clear()
	ax.set_xlabel('X [mm]')
	ax.set_ylabel('Y [mm]')
	ax.set_zlabel('Z [mm]')

	pose = bone.lerp_pose(val)
	points = bone.build_hand(pose, True)
	# Plot the Points
	bone.plot_steam_hand(points, "Lerped Pose", ax)

if __name__ == "__main__":
	p = multiprocessing.Process(target=serial_worker, args=(q,), daemon=True)
	p.start()
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=1)
	try:
		plt.show()
	except KeyboardInterrupt:
		quit()