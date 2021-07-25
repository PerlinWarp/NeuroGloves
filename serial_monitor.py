import serial
import time
import math

ser = serial.Serial('/dev/ttyUSB0', '115200')
time.sleep(1)

for i in range(0,1000):
    read = ser.readline()
    print(read)

    try:
        lineTable = read.decode().split('&')
        print( list(map(int,lineTable)) )
    except:
        print("WTF", read)


ser.close()