# win32Pipe
'''
https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes
'''
import struct, time
import win32pipe, win32file, win32con, pywintypes

class NamedPipe:
	def __init__(self, right_hand=True):
		if right_hand:
			# OpenGloves /named-pipe-communication-manager/src/DeviceProvider.cpp#L77
			self.pipename = r'\\.\\pipe\\vrapplication\\input\\right'
		else:
			self.pipename = r'\\.\\pipe\\vrapplication\\input\\left'
		self.fingers = [False]*5
		self.joys = [0.0, 0.0]
		self.buttons = [False]*8

	def encode(self, flexion, joys=None, bools=None):
		''' Struct format is from: https://github.com/LucidVR/opengloves-driver/.../EncodingManager.h#L17
	  const std::array<float, 5> flexion; // Between 0 and 1
	  const float joyX;     // Between -1 and 1
	  const float joyY;
	  const bool joyButton; // 0
	  const bool trgButton; // 1
	  const bool aButton;   // 2
	  const bool bButton;   // 3
	  const bool grab;      // 4
	  const bool pinch;     // 5
	  const bool menu;      // 6 
	  const bool calibrate; // 7
		'''
		if joys is not None:
			print(joys)
			joyX = joys[0]
			joyY = joys[1]
		else:
			joyX = 0.0
			joyY = 0.0
		
		if bools is None:
			bools = [False, False, False, False, False, False, False, False] 

		# https://tuttlem.github.io/2016/04/06/packing-data-with-python.html
		pack_obj = struct.pack('@5f', flexion[0], flexion[1], flexion[2], flexion[3], flexion[4])
		joys = struct.pack('@2f', joyX, joyY)
		pack_bools = struct.pack('@8?', *bools)
		pack_obj = pack_obj + joys + pack_bools
		return pack_obj

	def send(self, fingers, joys=None, bools=None):
		encoded = self.encode(fingers, joys, bools)
		try:
			# https://github.com/LucidVR/opengloves-driver/blob/develop/overlay/main.cpp#L128
			open_mode = win32con.GENERIC_READ | win32con.GENERIC_WRITE

			pipe = win32file.CreateFile(self.pipename,
											 open_mode,
											 0, # no sharing
											 None, # default security
											 win32con.OPEN_EXISTING,
											 0, # win32con.FILE_FLAG_OVERLAPPED,
											 None)
			win32file.WriteFile(pipe, encoded)
			win32file.CloseHandle(pipe)
		except pywintypes.error:
			print("Pipe busy")


if __name__ == "__main__":
	ipc_right = NamedPipe(right_hand=True)
	ipc_left = NamedPipe(right_hand=False)

	try:
		for i1 in range(0,10):
			for i2 in range(0,10):
				for i3 in range(0,10):
					for i4 in range(0,10):
						for i5 in range(0,10):
							fingers = [i1/10, i2/10, i3/10, i4/10, i5/10]
							bools = [True]*8
							bools[6] = True
							ipc_left.send(fingers, bools=bools)
							ipc_right.send(fingers, bools=bools)
							
							time.sleep(0.01)
							print(f"Wrote {fingers} to IPC")
	except KeyboardInterrupt:
		print("Quitting")
		
		quit()