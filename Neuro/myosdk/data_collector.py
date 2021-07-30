import serial

COM_PORT = "COM8"

ser = serial.Serial(COM_PORT,'115200', timeout=1)  # open serial port

print("Listening on "+COM_PORT)


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

while True:
	try:
	    read = ser.readline()
	    fingers = decode_serial(read)
	    print(fingers)
	except KeyboardInterrupt:
		print("Breaking...")
		ser.close()
		quit()