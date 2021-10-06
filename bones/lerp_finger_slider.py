import numpy as np
import bone
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

RESET_SCALE = True
a0 = 1.0

# Select which poses we want to lerp between
open_pose = bone.right_open_pose
closed_pose = bone.right_fist_pose

if __name__ == "__main__":
	# Get something to plot initially
	pose = bone.lerp_pose(0.2)
	points = bone.build_hand(pose, True)
	print("Built hand", points.shape)

	# Plot Setup
	fig = plt.figure("Finger Plots",figsize=(10, 10), dpi=100)
	ax = fig.add_subplot(111, projection='3d')
	plt.subplots_adjust(left=0.25, bottom=0.40)
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	# Slider setup
	ax.margins(x=0)
	axcolor = 'lightgoldenrodyellow'
	axamp = plt.axes([0.25, 0.30, 0.65, 0.03], facecolor=axcolor)
	ax_thumb = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
	ax_index = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
	ax_middle = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
	ax_ring = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
	ax_pinky = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
	# Add the sliders
	samp = Slider(axamp, 'All', 0.1, 1.5, valinit=a0)
	sthumb = Slider(ax_thumb, 'Thumb', 0.1, 1.5, valinit=a0)
	sindex = Slider(ax_index, 'Index', 0.1, 1.5, valinit=a0)
	smiddle = Slider(ax_middle, 'Middle', 0.1, 1.5, valinit=a0)
	sring = Slider(ax_ring, 'Ring', 0.1, 1.5, valinit=a0)
	spinky = Slider(ax_pinky, 'Pinky', 0.1, 1.5, valinit=a0)


	# Plot the Points
	x = points[:,0]
	y = points[:,1]
	z = points[:,2]
	ax.scatter(x,y,z)

	def update(val):
		ax.clear()
		ax.set_xlabel('X [mm]')
		ax.set_ylabel('Y [mm]')
		ax.set_zlabel('Z [mm]')
		
		if (RESET_SCALE == True):
			ax.set_xlim3d([-0.05, 0.1])
			ax.set_ylim3d([-0.1, 0.1])
			ax.set_zlim3d([0, 0.2])

		# Read the sliders
		amp = samp.val
		fingers = [sthumb.val, sindex.val, smiddle.val, sring.val, spinky.val]

		points = bone.lerp_fingers(fingers, bone.right_open_pose, bone.right_fist_pose)
		# Plot the Points
		bone.plot_steam_hand(points, "Lerped Pose", ax)

		fig.canvas.draw_idle()

	def update_curl(val):
		ax.clear()
		ax.set_xlabel('X [mm]')
		ax.set_ylabel('Y [mm]')
		ax.set_zlabel('Z [mm]')
		
		if (RESET_SCALE == True):
			ax.set_xlim3d([-0.05, 0.1])
			ax.set_ylim3d([-0.1, 0.1])
			ax.set_zlim3d([0, 0.2])

		# Read the slider
		amp = samp.val

		pose = bone.lerp_pose(amp, open_pose, closed_pose)
		points = bone.build_hand(pose, True)
		# Plot the Points
		bone.plot_steam_hand(points, "Lerped Pose", ax)

		fig.canvas.draw_idle()

	samp.on_changed(update_curl)
	sthumb.on_changed(update)
	sindex.on_changed(update)
	smiddle.on_changed(update)
	sring.on_changed(update)
	spinky.on_changed(update)


	def reset(event):
		samp.reset()

	def colorfunc(label):
		l.set_color(label)
		fig.canvas.draw_idle()

	plt.show()