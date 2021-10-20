if __name__ == "__main__":
	import serial
	# Check your COM Port in Windows Device Manager
	COM_PORT = "COM9"
	ser = serial.Serial(COM_PORT,'115200', timeout=1)  # open serial port

	print("Listening on "+COM_PORT)

	while True:
		try:
		    read = ser.readline()
		    print(read)
		except KeyboardInterrupt:
			print("Breaking...")
			ser.close()
			quit()