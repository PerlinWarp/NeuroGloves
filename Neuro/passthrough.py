import serial

# Arguments
GLOVE_COM_PORT = "COM8"
STEAM_COM_PORT = "COM6"

if __name__ == '__main__':
	glove_ser = serial.Serial(GLOVE_COM_PORT,'115200')  # Serial Port from Glove Arduino
	steam_ser = serial.Serial(STEAM_COM_PORT,'115200')  # OpenGloves output port

	while True:
		try:
			read = glove_ser.readline()
			print(read)
			steam_ser.write(read)
		except KeyboardInterrupt:
			glove_ser.close()