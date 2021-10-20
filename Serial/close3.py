import serial

ser = serial.Serial('COM3', 115200)
if not ser.isOpen():
    ser.open()
print('com3 is open', ser.isOpen())