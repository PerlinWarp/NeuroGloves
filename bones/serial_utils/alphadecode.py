import re

f = open("alphaencodings.txt","r")

alpha_chars = ["A", "B", "C", "D", "E"]

def decode_alpha(x):
	if (x == ''):
		return [0,0,0,0,0]
	else:
		# Split between numbers and letters
		x = re.split('(\d+)', x.rstrip())
		# Pull the flexion data out, Get rid of all other data than fingers
		fingers = [x[1], x[3], x[5], x[7], x[9]]
		# Cast to ints
		s = [int(f) for f in fingers]
		return s

for x in f:
	print(decode_alpha(x))