import serial
ser = serial.Serial('COM7','115200', timeout=1)  # open serial port

print("Listening on COM7")

while True:
	try:
	    read = ser.readline()
	    print(read)
	except KeyboardInterrupt:
		print("Breaking...")
		ser.close()
		quit()