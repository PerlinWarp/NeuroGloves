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
fig = plt.figure("Serial Finger Plots")
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
# Set the scale once
ax.set_xlim3d([-0.05, 0.1])
ax.set_ylim3d([-0.1, 0.1])
ax.set_zlim3d([0, 0.2])

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

	# Plot
	ax.clear()
	ax.set_xlabel('X [mm]')
	ax.set_ylabel('Y [mm]')
	ax.set_zlabel('Z [mm]')
	if (RESET_SCALE == True):
		ax.set_xlim3d([-0.05, 0.1])
		ax.set_ylim3d([-0.1, 0.1])
		ax.set_zlim3d([0, 0.2])

	# Turn finger values into Lerp Vals
	thumb_val = fingers[0] / 1024
	index_val = fingers[1] / 1024
	middle_val = fingers[2] / 1024
	ring_val = fingers[3] / 1024
	pinky_val = fingers[4] / 1024
	print("Fingers", fingers)
	fingers = [thumb_val, index_val, middle_val, ring_val, pinky_val]
	# Lerp the right hand
	points = bone.lerp_fingers(fingers, bone.right_open_pose, bone.right_fist_pose)

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