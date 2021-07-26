import serial
ser = serial.Serial('COM6','115200')  # open serial port
print("Writing to", ser.name)         # check which port was really used
ser.write(b'hello\n')     # write a string

def pack_vals(arr):
    # arr should be of length 13
    return b"%d&%d&%d&%d&%d&%d&%d&%d&%d&%d&%d&%d&%d\n" % tuple(arr)

def main():
    while True:
        try:
            for i in range(0,1024):
                vals = pack_vals([i]*13)
                print(vals)
                ser.write(vals)
        except KeyboardInterrupt:
            print("Ending...")
            ser.close()             # close port
            quit()

if __name__ == '__main__':
    main()
    quit()