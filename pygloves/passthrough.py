import serial
import time

# Arguments
GLOVE_COM_PORT = "COM9" # Check this in windows device manager
STEAM_COM_PORT = "COM6"

if __name__ == '__main__':
	glove_ser = serial.Serial(GLOVE_COM_PORT,'115200')  # Serial Port from Glove Arduino
	steam_ser = serial.Serial(STEAM_COM_PORT,'115200')  # OpenGloves output port
	time.sleep(3)
	steam_ser.write(b"\n")
	steam_ser.flush()
	glove_ser.flush()
	steam_ser.flushInput()
	glove_ser.flushInput()

	while True:
		try:
			read = glove_ser.readline()
			print(read, type(read))
			steam_ser.write(read)
		except KeyboardInterrupt:
			print("Exiting...")
			glove_ser.flush()
			glove_ser.close()
			steam_ser.close()