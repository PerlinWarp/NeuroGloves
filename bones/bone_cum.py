import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

'''
https://github.com/ValveSoftware/openvr/wiki/Hand-Skeleton
https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion
Example glb from OpenGloves, originally from steamvr/drivers/indexcontroller
Steam's OpenVR Uses (w,z,y,z) for Quaternions as defined in HmdQuaternionf_t

0 RootNode, 
1 REF:Root, 
2 REF:wrist_r, # All metacarpal positons are relative to this. 
3 REF:finger_thumb_0_r, 
4 REF:finger_thumb_1_r,
5 REF:finger_thumb_2_r,
6 REF:finger_thumb_r_end,
7 REF:finger_index_meta_r - -0.000632452196441591, 0.0268661547452211, 0.01500194799155
8 REF:finger_index_0_r
9 REF:finger_index_1_r
10 REF:finger_index_2_r
11 REF:finger_index_r_end
12 REF:finger_middle_meta_r  -0.00217731343582273, 0.00711954385042191, 0.0163187384605408
13 REF:finger_middle_0_r
14 REF:finger_middle_1_r
15 REF:finger_middle_2_r
16 REF:finger_middle_r_end
17 REF:finger_ring_meta_r -0.000513435574248433, -0.00654512271285057, 0.0163476932793856
18 REF:finger_ring_0_r
19 REF:finger_ring_1_r
20 REF:finger_ring_2_r
21 REF:finger_ring_r_end
22 REF:finger_pinky_meta_r 0.00247815088368952, -0.0189813692122698, 0.0152135835960507
23 REF:finger_pinky_0_r
24 REF:finger_pinky_1_r
25 REF:finger_pinky_2_r
26 REF:finger_pinky_r_end
27 REF:finger_thumb_r_aux -0.00605911063030362, 0.0562852211296558, -0.0600638426840305
28 REF:finger_index_r_aux
29 REF:finger_middle_r_aux
30 REF:finger_ring_r_aux
31 REF:finger_pinky_r_aux
'''

right_pose = np.array([
	# Position{HmdVector4_t} (x,y,z,1) , Quaternion{HmdQuaternionf_t} (w,x,y,z)
	# https://github.com/ValveSoftware/openvr/issues/505
	[[0.000000, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]], # 0 - Root Node, Dan Skipped the Ref:Root
	[[0.034038, 0.036503, 0.164722, 1.000000], [-0.055147, -0.078608, 0.920279, -0.379296]], # 2 - Wrist
	[[0.012083, 0.028070, 0.025050, 1.000000], [0.567418, -0.464112, 0.623374, -0.272106]], # Thumb Meta
	[[-0.040406, -0.000000, 0.000000, 1.000000], [0.994838, 0.082939, 0.019454, 0.055130]],
	[[-0.032517, -0.000000, -0.000000, 1.000000], [0.974793, -0.003213, 0.021867, -0.222015]],
	[[-0.030464, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]],
	[[-0.000632, 0.026866, 0.015002, 1.000000], [0.421979, -0.644251, 0.422133, 0.478202]], # Index Meta
	[[-0.074204, 0.005002, -0.000234, 1.000000], [0.995332, 0.007007, -0.039124, 0.087949]],
	[[-0.043930, 0.000000, 0.000000, 1.000000], [0.997891, 0.045808, 0.002142, -0.045943]],
	[[-0.028695, -0.000000, -0.000000, 1.000000], [0.999649, 0.001850, -0.022782, -0.013409]],
	[[-0.022821, -0.000000, 0.000000, 1.000000], [1.000000, -0.000000, 0.000000, -0.000000]],
	[[-0.002177, 0.007120, 0.016319, 1.000000], [0.541276, -0.546723, 0.460749, 0.442520]], # Middle Meta
	[[-0.070953, -0.000779, -0.000997, 1.000000], [0.980294, -0.167261, -0.078959, 0.069368]],
	[[-0.043108, -0.000000, -0.000000, 1.000000], [0.997947, 0.018493, 0.013192, 0.059886]],
	[[-0.033266, -0.000000, -0.000000, 1.000000], [0.997394, -0.003328, -0.028225, -0.066315]],
	[[-0.025892, 0.000000, -0.000000, 1.000000], [0.999195, -0.000000, 0.000000, 0.040126]],
	[[-0.000513, -0.006545, 0.016348, 1.000000], [0.550143, -0.516692, 0.429888, 0.495548]], # Ring Meta
	[[-0.065876, -0.001786, -0.000693, 1.000000], [0.990420, -0.058696, -0.101820, 0.072495]],
	[[-0.040697, -0.000000, -0.000000, 1.000000], [0.999545, -0.002240, 0.000004, 0.030081]],
	[[-0.028747, 0.000000, 0.000000, 1.000000], [0.999102, -0.000721, -0.012693, 0.040420]],
	[[-0.022430, 0.000000, -0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]], 
	[[0.002478, -0.018981, 0.015214, 1.000000], [0.523940, -0.526918, 0.326740, 0.584025]], # Pinky Meta
	[[-0.062878, -0.002844, -0.000332, 1.000000], [0.986609, -0.059615, -0.135163, 0.069132]],
	[[-0.030220, -0.000000, -0.000000, 1.000000], [0.994317, 0.001896, -0.000132, 0.106446]],
	[[-0.018187, -0.000000, -0.000000, 1.000000], [0.995931, -0.002010, -0.052079, -0.073526]],
	[[-0.018018, -0.000000, 0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]],
	# https://github.com/ValveSoftware/openvr/wiki/Hand-Skeleton#auxiliary-bones
	[[0.006059, 0.056285, 0.060064, 1.000000], [0.737238, 0.202745, -0.594267, -0.249441]], # thumb aux
	[[0.040416, -0.043018, 0.019345, 1.000000], [-0.290331, 0.623527, 0.663809, 0.293734]], # index aux
	[[0.039354, -0.075674, 0.047048, 1.000000], [-0.187047, 0.678062, 0.659285, 0.265683]], # middle aux
	[[0.038340, -0.090987, 0.082579, 1.000000], [-0.183037, 0.736793, 0.634757, 0.143936]], # ring aux
	[[0.031806, -0.087214, 0.121015, 1.000000], [-0.003659, 0.758407, 0.639342, 0.126678]], # pinky aux
])

right_fist_pose = np.array([
	[[0.000000, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]],
	[[0.034038, 0.036503, 0.164722, 1.000000], [-0.055147, -0.078608, 0.920279, -0.379296]],
	[[0.016305, 0.027529, 0.017800, 1.000000], [0.483332, -0.225703, 0.836342, -0.126413]],
	[[-0.040406, -0.000000, 0.000000, 1.000000], [0.894335, -0.013302, -0.082902, 0.439448]],
	[[-0.032517, -0.000000, -0.000000, 1.000000], [0.842428, 0.000655, 0.001244, 0.538807]],
	[[-0.030464, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]],
	[[-0.003802, 0.021514, 0.012803, 1.000000], [0.395174, -0.617314, 0.449185, 0.510874]],
	[[-0.074204, 0.005002, -0.000234, 1.000000], [0.737291, -0.032006, -0.115013, 0.664944]],
	[[-0.043287, 0.000000, 0.000000, 1.000000], [0.611381, 0.003287, 0.003823, 0.791321]],
	[[-0.028275, -0.000000, -0.000000, 1.000000], [0.745388, -0.000684, -0.000945, 0.666629]],
	[[-0.022821, -0.000000, 0.000000, 1.000000], [1.000000, -0.000000, 0.000000, -0.000000]],
	[[-0.005787, 0.006806, 0.016534, 1.000000], [0.522315, -0.514203, 0.483700, 0.478348]],
	[[-0.070953, -0.000779, -0.000997, 1.000000], [0.723653, -0.097901, 0.048546, 0.681458]],
	[[-0.043108, -0.000000, -0.000000, 1.000000], [0.637464, -0.002366, -0.002831, 0.770472]],
	[[-0.033266, -0.000000, -0.000000, 1.000000], [0.658008, 0.002610, 0.003196, 0.753000]],
	[[-0.025892, 0.000000, -0.000000, 1.000000], [0.999195, -0.000000, 0.000000, 0.040126]],
	[[-0.004123, -0.006858, 0.016563, 1.000000], [0.523374, -0.489609, 0.463997, 0.520644]],
	[[-0.065876, -0.001786, -0.000693, 1.000000], [0.759970, -0.055609, 0.011571, 0.647471]],
	[[-0.040331, -0.000000, -0.000000, 1.000000], [0.664315, 0.001595, 0.001967, 0.747449]],
	[[-0.028489, 0.000000, 0.000000, 1.000000], [0.626957, -0.002784, -0.003234, 0.779042]],
	[[-0.022430, 0.000000, -0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]],
	[[-0.001131, -0.019295, 0.015429, 1.000000], [0.477833, -0.479766, 0.379935, 0.630198]],
	[[-0.062878, -0.002844, -0.000332, 1.000000], [0.827001, 0.034282, 0.003440, 0.561144]],
	[[-0.029874, -0.000000, -0.000000, 1.000000], [0.702185, -0.006716, -0.009289, 0.711903]],
	[[-0.017979, -0.000000, -0.000000, 1.000000], [0.676853, 0.007956, 0.009917, 0.736009]],
	[[-0.018018, -0.000000, 0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]],
	[[-0.019716, 0.002802, 0.093937, 1.000000], [0.377286, -0.540831, -0.150446, 0.736562]],
	[[-0.000171, 0.016473, 0.096515, 1.000000], [-0.006456, 0.022747, 0.932927, 0.359287]],
	[[-0.000448, 0.001536, 0.116543, 1.000000], [-0.039357, 0.105143, 0.928833, 0.353079]],
	[[-0.003949, -0.014869, 0.130608, 1.000000], [-0.055071, 0.068695, 0.944016, 0.317933]],
	[[-0.003263, -0.034685, 0.139926, 1.000000], [0.019690, -0.100741, 0.957331, 0.270149]],
])

def quaternion_multiply(quaternion1, quaternion0):
	# Computes the Hamilton product
	w0, x0, y0, z0 = quaternion0
	w1, x1, y1, z1 = quaternion1
	return np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
					 x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
					 -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
					 x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float64)

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return np.array([w, x, y, z])

def build_pose(pose):
	'''
	Converts the relative points in SteamHand to global points by building the hand
	'''

	c = pose[:,0,:3]
	q = pose[:,1,:]
	print(c.shape)
	print(q.shape)
	# Wrist
	wirst = c[1]
	xs = [wirst[0]]
	ys = [wirst[1]]
	zs = [wirst[2]]
	# get the x,y,z rotated coordinates of the pose
	# Seperate the fingers
	thumb = pose[2:6, :, :]
	index = pose[6:11, :,:]
	middle = pose[11:16, :,:]
	ring = pose[16:21, :, :]
	pinky = pose[21:26, :, :]

	# Read the file format into x,y,z and build the hand
	fingers = [thumb, index, middle, ring, pinky]
	for finger in fingers:

		# Use the wrist the first time
		x = wirst[0]
		y = wirst[1]
		z = wirst[2]

		quat = pose[:,1,:][1]
		print("Wrist Quat", quat)
		for row in finger:
			print("Row", row)
			c = row[0,:]
			q = row[1,:]
			print(c)

			# Calculate cumulative rotation
			quat = q_mult(quat, q)

			# Rotate the position
			x, y, z, w = quat
			sp_x, sp_y, sp_z, one  = c

			vec = [0, sp_x, sp_z, sp_y]
			r = [w, x, y, z]
			# Calculate the Quaternion Conjugate
			r_c = [w, -x, -y, -z]
			# Rotate the point
			#rotated_point = quaternion_multiply(quaternion_multiply(r, vec), r_c)
			# Due to quaternion representation, the first element will always be 0
			rotated_point = q_mult(q_mult(r, vec), r_c)[1:]
			print("Rotated p:, ",rotated_point)

			# Position = position + parent
			x += rotated_point[0]
			y += rotated_point[1]
			z += rotated_point[2]
			xs.append(x)
			ys.append(y)
			zs.append(z)

	hand_points = np.array([xs, ys, zs]).T
	hand = hand_points

	# Plot the hand
	# Plot setup
	fig = plt.figure("Cum Hand")
	ax = fig.add_subplot(111, projection='3d', xlim=(-0.2, 0.2), ylim=(-0.2, 0.2), zlim=(0, 0.4))
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')
	hand = np.array(hand)
	print("hps", hand.shape)

	xs = hand[:,0]
	ys = hand[:,1]
	zs = hand[:,2]
	ax.scatter(xs,ys,zs)
	plt.show()

	return hand_points


# def build_pose(pose, i=0, last_row=[], hand=[]):
# 	print("i", i)
# 	if (i == 31):
# 		# Plot the hand
# 		# Plot setup
# 		fig = plt.figure("Cum Hand")
# 		ax = fig.add_subplot(111, projection='3d', xlim=(-0.2, 0.2), ylim=(-0.2, 0.2), zlim=(0, 0.4))
# 		ax.set_xlabel('X [m]')
# 		ax.set_ylabel('Y [m]')
# 		ax.set_zlabel('Z [m]')
# 		hand = np.array(hand)
# 		print("hps", hand.shape)

# 		xs = hand[:,0]
# 		ys = hand[:,1]
# 		zs = hand[:,2]
# 		ax.scatter(xs,ys,zs)
# 		plt.show()
# 		return hand
# 	else:	
# 		# Read this row
# 		row = pose[i,:]
# 		# Coordinate, Quaternion
# 		c, q = row
# 		w, x, y, z = q
# 		sp_x, sp_y, sp_z, one  = c

# 		if (i == 0):
# 			# Root / Wrist
# 			hand.append(c)
# 			return build_pose(pose, i+1, row, hand)
# 		else:
# 			# Multiply vector by Quaternion
# 			vec = [0, sp_x, sp_z, sp_y]
# 			r = [w, x, y, z]
# 			# Calculate the Quaternion Conjugate
# 			r_c = [w, -x, -y, -z]
# 			# Rotate the point
# 			#rotated_point = quaternion_multiply(quaternion_multiply(r, vec), r_c)
# 			rotated_point = q_mult(q_mult(r, vec), r_c)

# 			if (i == 1): # Wrist
# 				hand.append(rotated_point)
# 				return build_pose(pose, i+1, row, hand)
# 			elif (i < 7):
# 				# Thumb
# 				return build_pose(pose, i+1, row, hand)
# 			else:
# 				# Finger
# 				return build_pose(pose, i+1, row, hand)

# 		# Seperate the fingers
# 		thumb = row[2:6, :]
# 		index = row[6:11, :]
# 		middle = row[11:16, :]
# 		ring = row[16:21, :]
# 		pinky = row[21:26, :]

# 		quit()

def rotate_pose(pose):
	'''
	For all the points in the hand
	we rotate by the quaternion
	returns rotated points
	See: https://www.meccanismocomplesso.org/en/hamiltons-quaternions-and-3d-rotation-with-python/
	'''
	# x,y,z coordinates of the pose
	rotated_points = []

	for row in pose:
		c, q = row
		print("Steam Coordinates: ", c)
		# Convert Quaternion layout that glb uses
		x, y, z, w = q
		sp_x, sp_y, sp_z, one  = c
		'''
		In SteamVR
		+Y is up
		+X is to the right
		-Z is forward
		In MatplotLib
		+Z is up
		+Y is to the right
		-X is forward
		'''
		vec = [0, sp_x, sp_z, sp_y]
		r = [w, x, y, z]
		# Calculate the Quaternion Conjugate
		r_c = [w, -x, -y, -z]
		# Rotate the point
		#rotated_point = quaternion_multiply(quaternion_multiply(r, vec), r_c)
		rotated_point = q_mult(q_mult(r, vec), r_c)
		print("Rotated p:, ",rotated_point)
		# Due to quaternion representation, the first element will always be 0
		rotated_points.append(rotated_point[1:])
	rotated_points = np.array(rotated_points)
	#print(rotated_points)
	return rotated_points

def local_to_global_hand(points):
	'''
	Converts the relative points in SteamHand to global points by building the hand
	'''
	c = points
	# Add the wrist
	xs = [c[1][0]]
	ys = [c[1][1]]
	zs = [c[1][2]]
	# get the x,y,z rotated coordinates of the pose
	# Seperate the fingers
	thumb = c[2:6]
	index = c[6:11]
	middle = c[11:16]
	ring = c[16:21]
	pinky = c[21:26]

	# Read the file format into x,y,z and build the hand
	fingers = [thumb, index, middle, ring, pinky]
	for finger in fingers:
		# Use the wrist the first time
		x = c[1][0]
		y = c[1][1]
		z = c[1][2]

		for point in finger:
			x += point[0]
			y += point[1]
			z += point[2]
			xs.append(x)
			ys.append(y)
			zs.append(z)

	hand_points = np.array([xs, ys, zs]).T
	return hand_points

def plot_steam_hand_points(points, title="Steam Hand Points"):
	'''
	Expects the *relative* coordinates of a pose, not including the quaternions
	points.shape == (31, 3)
	'''
	# Plot setup
	fig = plt.figure(title)
	ax = fig.add_subplot(111, projection='3d', xlim=(-0.2, 0.2), ylim=(-0.2, 0.2), zlim=(0, 0.4))
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	hand_points = local_to_global_hand(points)
	print("hps", hand_points.shape)

	xs = hand_points[:,0]
	ys = hand_points[:,1]
	zs = hand_points[:,2]
	ax.scatter(xs,ys,zs)
	plt.show()


def plot_steam_hand(rel_points, title="Steam Hand"):
	'''
	Expects the *relative* coordinates of a pose, not including the quaternions
	points.shape == (31, 3)
	'''
	# Plot setup
	fig = plt.figure(title)
	ax = fig.add_subplot(111, projection='3d', xlim=(-0.2, 0.2), ylim=(-0.2, 0.2), zlim=(0, 0.4))
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	hand_points = local_to_global_hand(rel_points)
	xs = hand_points[:,0]
	ys = hand_points[:,1]
	zs = hand_points[:,2]
	print("Rel", rel_points.shape)
	print("Global", hand_points.shape)
	# Plot the Points that make up the hand
	ax.scatter(xs,ys,zs)

	# Draw lines between them
	# Seperate the fingers
	c = hand_points

	# Draw the thumb
	for n in [1,2,3]:
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color="lime")
		ax.add_line(l)
	# Index
	for n in range(5,9):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='firebrick')
		ax.add_line(l)
	# Middle
	for n in range(10,14):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='purple')
		ax.add_line(l)
	# Ring Finger
	for n in range(15,19):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='blue')
		ax.add_line(l)
	# Pinky finger
	for n in range(20,24):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='pink')
		ax.add_line(l)
	
	# Draw lines to connect the metacarpals
	for i in range(4):
		ms = [2, 6,11,16,21]
		l = plt3d.art3d.Line3D([c[ms[i],0], c[ms[i+1],0]], [c[ms[i],1], c[ms[i+1],1]], [c[ms[i],2], c[ms[i+1],2]], color="aqua")
		ax.add_line(l)
	# Draw lines to connect the hand
	for i in range(4):
		ms = [1, 5,10,15,20]
		l = plt3d.art3d.Line3D([c[ms[i],0], c[ms[i+1],0]], [c[ms[i],1], c[ms[i+1],1]], [c[ms[i],2], c[ms[i+1],2]], color="aqua")
		ax.add_line(l)
	# Connect the bottom of the hand together
	l = plt3d.art3d.Line3D([c[1,0], c[20,0]], [c[1,1], c[20,1]], [c[1,2], c[20,2]], color="aqua")
	ax.add_line(l)
	l = plt3d.art3d.Line3D([c[1,0], c[0,0]], [c[1,1], c[0,1]], [c[1,2], c[0,2]], color="aqua")
	ax.add_line(l)
	l = plt3d.art3d.Line3D([c[0,0], c[20,0]], [c[0,1], c[20,1]], [c[0,2], c[20,2]], color="aqua")
	ax.add_line(l)


	plt.show()

if __name__ == "__main__":
	pose_quards = right_fist_pose[:,0,:3]
	# Try building a hand from the glb only using the x,y,z
	#plot_steam_hand_points(pose_quards)
	build_pose(right_pose)
	quit()

	plot_steam_hand(pose_quards)

	# # rotates each point in the pose, around the origin by the quaternion then builds the hand
	right_fist_pose = rotate_pose(right_fist_pose)
	plot_steam_hand(right_fist_pose, "Right fist pose")
	right_pose = rotate_pose(right_pose)
	plot_steam_hand(right_pose, "Right Open pose")