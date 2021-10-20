import serial
import re

# Use device manager to find the Arduino's serial port.
COM_PORT = "COM9"
LEGACY_DECODE = False # If false, will use alpha encodings

def decode_legacy_serial(s):
	if s == b'':
		return [0,0,0,0,0]
	else:
		# Decode the byte string to list of ints
		s = s.decode().rstrip().split('&')
		# Get rid of all other data than fingers
		s = s[0:5]
		# Cast to ints
		s = [int(f) for f in s]
		return s

def decode_alpha_serial(s):
	if (s == b''):
		return [0,0,0,0,0]
	else:
		# Decode from bytes
		x = s.decode()
		# Split between numbers and letters
		x = re.split('(\d+)', x.rstrip())
		# Pull the flexion data out, Get rid of all other data than fingers
		fingers = [x[1], x[3], x[5], x[7], x[9]]
		# Cast to ints
		s = [int(f) for f in fingers]
		return s

if __name__ == "__main__":
	ser = serial.Serial(COM_PORT,'115200', timeout=1)  # open serial port
	print("Listening on "+COM_PORT)

	while True:
		try:
			read = ser.readline()
			if LEGACY_DECODE:
				fingers = decode_legacy_serial(read)
			else:
				fingers = decode_alpha_serial(read)
			print(fingers)
		except KeyboardInterrupt:
			print("Breaking...")
			ser.close()
			quit()