finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

def decode_serial(s):
	if s == b'':
		return None
	else:
		# Decode the byte string to list of ints
		s = s.decode().rstrip().split('&')
		# Get rid of all other data than fingers
		s = s[0:5]
		# Cast to ints
		s = [int(f) for f in s]
		return s