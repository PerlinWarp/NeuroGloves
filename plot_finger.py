import time

import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

# Serial Setup
ser = serial.Serial('/dev/ttyUSB0', '115200')
#time.sleep(1)


def on_close(event):
    print("Closed Figure")

    # Close the serial connection
    ser.close()

# Matplotlib Setup
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close)
ax = fig.add_subplot(111, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax.view_init(elev=45., azim=122)

NUM_POINTS = 2
points = np.zeros((3, NUM_POINTS))
patches = ax.scatter(points[0], points[1], points[2], s=[20]*NUM_POINTS, alpha=1)

def get_points():
    # Read from serial
    read = ser.readline()
    print(read)

    try:
        lineTable = read.decode().split('&')
        data =  list(map(int,lineTable))
        angle =  data[0]/1024
    except:
        print("WTF", read)
        angle = 0

    print(angle)

    X = [1, angle]
    Y = [1, angle]
    Z = [1, angle]


    return np.array([X, Z, Y])


def plot_points(points):
    patches.set_offsets(points[:2].T)
    patches.set_3d_properties(points[2], zdir='z')

def plot_lines(points):
    return None

def animate(i):
    # Reset the plot
    ax.cla()
    # Really you can just update the lines to avoid this
    ax.view_init(elev=45., azim=122)
    ax.set_xlim3d([0, 5])
    ax.set_xlabel('X [mm]')
    ax.set_ylim3d([0, 5])
    ax.set_ylabel('Y [mm]')
    ax.set_zlim3d([0, 5])
    ax.set_zlabel('Z [mm]')

    points = get_points()

    patches = ax.scatter(points[0], points[1], points[2], s=[10]*NUM_POINTS, alpha=1)
    plot_points(points)
    plot_lines(points)

    return patches,

def main():
    anim = animation.FuncAnimation(fig, animate, blit=False, interval=2)
    try:
        plt.show()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
