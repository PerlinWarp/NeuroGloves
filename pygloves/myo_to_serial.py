import multiprocessing

from myo_raw import MyoRaw

carryOn = True

# ------------ Myo Setup ---------------
q = multiprocessing.Queue()

m = MyoRaw(raw=False, filtered=True)
m.connect()

def worker(q):
	def add_to_queue(emg, movement):
		q.put(emg)

	m.add_emg_handler(add_to_queue)

	"""worker function"""
	while carryOn:
		m.run(1)
	print("Worker Stopped")

def print_battery(bat):
	print("Battery level:", bat)

m.add_battery_handler(print_battery)

 # Orange logo and bar LEDs
m.set_leds([128, 0, 0], [128, 0, 0])
# Vibrate to know we connected okay
m.vibrate(1)

# -------- Main Program Loop -----------
p = multiprocessing.Process(target=worker, args=(q,))
p.start()

try:
	while carryOn:
		while not(q.empty()):
			emg = list(q.get())
			print(emg)

except KeyboardInterrupt:
	print("Quitting")
	quit()