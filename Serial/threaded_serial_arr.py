import multiprocessing
import serial

import myo

# Serial Setup
COM_PORT = "COM8"

def decode_serial(s):
	if s == b'':
		return None
	else:
		# Decode the byte string to list of ints
		s = s.decode().rstrip().split('&')
		# Get rid of all other data than fingers
		s = s[0:5]
		# Cast to ints
		s = [int(f) for f in s]
		return s

def serial_worker(port, sarr):
	ser = serial.Serial(port,'115200', timeout=1)  # open serial port
	print("Listening on "+port)

	while True:
		try:
		    read = ser.readline()
		    fingers = decode_serial(read)
		    if fingers is not None:
		    	# Update the shared array
		    	for i in range(0,5):
		    		sarr[i] =  fingers[i]
		    else:
		    	print("None")
		except KeyboardInterrupt:
			print("Breaking...")
			ser.close()
			quit()

if __name__ == '__main__':
	arr = multiprocessing.Array('i', range(5))
	p = multiprocessing.Process(target=serial_worker, args=(COM_PORT, arr,))
	p.start()

	try:
		while True:
			fingers = list(arr)
			print("Glove:", fingers)

	except KeyboardInterrupt:
		print("Quitting")
		p.kill()
		quit()