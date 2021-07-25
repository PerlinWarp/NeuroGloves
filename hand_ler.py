import serial
import multiprocessing

def hand_ler(shared_arr):
	ser = serial.Serial('/dev/ttyUSB0', '115200')

	while True:
		read = ser.readline()

		try:
			lineTable = read.decode().split('&')
			data = list(map(int,lineTable))

			for i in range(len(data)):
				shared_arr[i] = data[i]

		except:
			continue



# -------- Main Program Loop -----------
if __name__ == '__main__':
	q = multiprocessing.Queue()
	p = multiprocessing.Process(target=hand_ler, args=(q,))
	p.start()

	while True:
		if ((not q.empty())):
			print(q.get())
		else:
			print("Empty")