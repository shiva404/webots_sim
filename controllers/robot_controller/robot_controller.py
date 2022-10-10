import os.path

from controller import Robot, Camera
import numpy as np
from datetime import datetime
import os

TIME_STEP = 64
robot = Robot()
ds = []
dsNames = ['ds_right', 'ds_left']
for i in range(2):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']

cm = robot.getDevice('cam')
cm.enable(TIME_STEP)

print(np.random.random(10))

for i in range(4):
    print(wheelsNames[i])
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0

BASE_DIR = '/home/shiv/Documents/plants_try/data/camera_images'
dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
images_dir = os.path.join(BASE_DIR, dt_string)
os.makedirs(images_dir)
image_number = 0

cm.recognitionEnable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    image_number += 1
    cm.saveImage(f"{os.path.join(images_dir, str(image_number))}_raw.jpg", 70)

    leftSpeed = 1.0
    rightSpeed = 1.0
    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        leftSpeed = 1.0
        rightSpeed = -1.0
    else:  # read sensors
        for i in range(2):
            if ds[i].getValue() < 950.0:
                avoidObstacleCounter = 100
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
