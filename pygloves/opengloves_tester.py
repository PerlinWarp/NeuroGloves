'''
Inside opengloves you need to be using the NamedPipe communication method with the right hand enabled.
Note this is made for the right hand.
'''
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from pygloves_utils import serial_utils as s
from pygloves_utils import bone

RESET_SCALE = True
a0 = 1.0

# Select which poses we want to lerp between
open_pose = bone.right_open_pose
closed_pose = bone.right_fist_pose
ipc_bools = [False, False, False, False, False, False, False, False]

if __name__ == "__main__":
	# IPC Setup
	ipc = s.ipc.NamedPipe()

	# Get something to plot initially
	pose = bone.lerp_pose(0.2)
	points = bone.build_hand(pose, True)
	print("Built hand", points.shape)

	# Plot Setup
	fig = plt.figure("Finger Plots",figsize=(10, 10), dpi=100)
	ax = fig.add_subplot(111, projection='3d')
	plt.subplots_adjust(left=0.25, bottom=0.50)
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')
	ax.view_init(elev=25, azim=-150)

	# Slider setup
	ax.margins(x=0)
	axcolor = 'lightgoldenrodyellow'
	axamp = plt.axes([0.25, 0.40, 0.50, 0.03], facecolor=axcolor)
	ax_thumb = plt.axes([0.25, 0.35, 0.50, 0.03], facecolor=axcolor)
	ax_index = plt.axes([0.25, 0.30, 0.50, 0.03], facecolor=axcolor)
	ax_middle = plt.axes([0.25, 0.25, 0.50, 0.03], facecolor=axcolor)
	ax_ring = plt.axes([0.25, 0.20, 0.50, 0.03], facecolor=axcolor)
	ax_pinky = plt.axes([0.25, 0.15, 0.50, 0.03], facecolor=axcolor)
	ax_joy_x = plt.axes([0.25, 0.10, 0.50, 0.03], facecolor=axcolor)
	ax_joy_y = plt.axes([0.25, 0.05, 0.50, 0.03], facecolor=axcolor)


	# Add the sliders
	samp = Slider(axamp, 'All', 0.0, 1.0, valinit=a0)
	sthumb = Slider(ax_thumb, 'Thumb', 0.0, 1.0, valinit=a0)
	sindex = Slider(ax_index, 'Index', 0.0, 1.0, valinit=a0)
	smiddle = Slider(ax_middle, 'Middle', 0.0, 1.0, valinit=a0)
	sring = Slider(ax_ring, 'Ring', 0.0, 1.0, valinit=a0)
	spinky = Slider(ax_pinky, 'Pinky', 0.0, 1.0, valinit=a0)
	sjoy_x = Slider(ax_joy_x, 'Joy X', -1.0, 1.0, valinit=0.0)
	sjoy_y = Slider(ax_joy_y, 'Joy Y', -1.0, 1.0, valinit=0.0)

	# Button Setup
	ax_joyb =    plt.axes([0.8, 0.40, 0.1, 0.03])
	ax_trigger = plt.axes([0.8, 0.35, 0.1, 0.03])
	ax_a =       plt.axes([0.8, 0.30, 0.1, 0.03])
	ax_b =       plt.axes([0.8, 0.25, 0.1, 0.03])
	ax_grab =    plt.axes([0.8, 0.20, 0.1, 0.03])
	ax_pinch =   plt.axes([0.8, 0.15, 0.1, 0.03])
	ax_menu =    plt.axes([0.8, 0.10, 0.1, 0.03])

	# Add the button
	joy_button = Button(ax_joyb, 'Joy Click', color=axcolor, hovercolor='0.975')
	trigger_button = Button(ax_trigger, 'Trigger', color=axcolor, hovercolor='0.975')
	a_button = Button(ax_a, 'A', color=axcolor, hovercolor='0.975')
	b_button = Button(ax_b, 'B', color=axcolor, hovercolor='0.975')
	grab_button = Button(ax_grab, 'Grab', color=axcolor, hovercolor='0.975')
	pinch_button = Button(ax_pinch, 'Pinch', color=axcolor, hovercolor='0.975')
	menu_button = Button(ax_menu, 'Menu', color=axcolor, hovercolor='0.975')

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
		joys = [sjoy_x.val, sjoy_y.val]
		print("Fingers", fingers, "Joys", joys)
		ipc.send(fingers, joys, ipc_bools)

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
		ipc.send([amp]*5, bools=ipc_bools)

		pose = bone.lerp_pose(amp, open_pose, closed_pose)
		points = bone.build_hand(pose, True)
		# Plot the Points
		bone.plot_steam_hand(points, "Lerped Pose", ax)

		fig.canvas.draw_idle()

	def button_updates(event, num=0):
		'''
	      const bool joyButton; // 0
		  const bool trgButton; // 1
		  const bool aButton;   // 2
		  const bool bButton;   // 3
		  const bool grab;      // 4
		  const bool pinch;     // 5
		  const bool menu;      // 6 
		  const bool calibrate; // 7
		'''
		print("Pressed button: ", num)
		fingers = [sthumb.val, sindex.val, smiddle.val, sring.val, spinky.val]
		joys = [sjoy_x.val, sjoy_y.val]
		# Click or unclick the button
		ipc_bools[num] = not ipc_bools[num]
		print(f"Button {num} is {ipc_bools[num]}")
		ipc.send(fingers, joys, ipc_bools)

	# Slider updates
	samp.on_changed(update_curl)
	sthumb.on_changed(update)
	sindex.on_changed(update)
	smiddle.on_changed(update)
	sring.on_changed(update)
	spinky.on_changed(update)
	sjoy_x.on_changed(update)
	sjoy_y.on_changed(update)


	# Button Updates
	joy_button.on_clicked(lambda event: button_updates(event, num=0))
	trigger_button.on_clicked(lambda event: button_updates(event, num=1))
	a_button.on_clicked(lambda event: button_updates(event, num=2))
	b_button.on_clicked(lambda event: button_updates(event, num=3))
	grab_button.on_clicked(lambda event: button_updates(event, num=4))
	pinch_button.on_clicked(lambda event: button_updates(event, num=5))
	menu_button.on_clicked(lambda event: button_updates(event, num=6))

	def reset(event):
		samp.reset()

	def colorfunc(label):
		l.set_color(label)
		fig.canvas.draw_idle()

	plt.show()