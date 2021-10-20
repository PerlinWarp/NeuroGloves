def encode_legacy_serial(fingers, grab=0, pinch=0):
	arr = fingers+[grab, pinch]
	# arr should be of length 13
	'''
	0 - 4 - flexion
	5 - JoyX - Default at 512?
	6 - JoyY
	...
	12 - grab 0/1
	13 - pinch 0/1
	'''
	return b"%d&%d&%d&%d&%d&521&521&0&0&0&0&%d&%d\n" % tuple(arr)

def encode_alpha_serial(fingers):
	'''
	https://github.com/LucidVR/lucidgloves/blob/main/firmware/lucidgloves-firmware/Encoding.ino#L44
	'''
	joyx = 512
	joyy = 512
	options = [joyx, joyy]
	arr = fingers+options

	return b"A%dB%dC%dD%dE%dF%dG%d\n" % tuple(arr)
	