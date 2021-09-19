import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import pygloves as pg

ser = serial.Serial('COM7','115200')  # open serial port

print("Listening on COM7")

def on_close(event):
	print("Closed Figure")
	ser.close()
	quit()

# Matplotlib Setup
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close)
ax1 = fig.add_subplot(1,1,1)

def animate(i):
	read = ser.readline()
	s = pg.decode_serial(read)
	s = np.array(s)
	print(s)

	ax1.clear()
	ax1.bar(pg.finger_names,s)
	ser.flushInput()

def main():
	ser.flushInput()
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=2)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
