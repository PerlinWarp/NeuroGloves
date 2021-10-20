import serial
import time

# Steam is listening on port 7 for the glove right hand
# We set this in open gloves
STEAM_COM_PORT = "COM7"

if __name__ == '__main__':
	steam_ser = serial.Serial(STEAM_COM_PORT,'115200')  # OpenGloves output port
	time.sleep(3)
	steam_ser.write(b"\n")
	steam_ser.flush()
	steam_ser.flushInput()
	print("Starting to read:", STEAM_COM_PORT)
	while True:
		try:
			read = steam_ser.readline()
			print(read, type(read))
		except KeyboardInterrupt:
			print("Exiting...")
			steam_ser.flush()
			steam_ser.close()