import serial
import time
import math

ser = serial.Serial('/dev/ttyUSB0', '115200')
time.sleep(3)
ser.write(b'READ_VALUES\n')
#start = float(ser.readline()) / 200

for x in range(3):
    for y in range(100):
        ser.write(b'READ_VALUES\n')
        read = ser.readline()
        print(read)
        lineTable = read.decode().split(',')
        for fing in range(5):
            thisVal = float(lineTable[fing].rstrip())
            current = ((highLimit[fing] - thisVal) * actuationAngle[fing]/ (highLimit[fing]-lowLimit[fing]))
            if (current < 0):
                current = 0 


ser.close()