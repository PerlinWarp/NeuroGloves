import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

ser = serial.Serial('COM9','115200')  # open serial port

def decode_serial(s):
	if s == b'':
		print(s)
	else:
		# Decode the byte string to list of ints
		s = s.decode().rstrip().split('&')
		# Get rid of all other data than fingers
		s = s[0:5]
		# Cast to ints
		s = [int(f) for f in s]
		return s

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
	s = decode_serial(read)
	s = np.array(s)
	print(s)

	ax1.clear()
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