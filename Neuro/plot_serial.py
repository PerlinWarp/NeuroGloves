import serial

import pyglove as pg

ser = serial.Serial('COM7','115200')  # open serial port

print("Listening on COM7")

while True:
	try:
	    read = ser.readline()
	    s = pg.decode_serial(read)
	    print(s)
	except KeyboardInterrupt:
		print("Breaking...")
		ser.close()
		quit()