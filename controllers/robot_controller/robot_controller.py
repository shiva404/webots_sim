from controller import Robot, Camera, CameraRecognitionObject
import numpy as np
from datetime import datetime
import os
from camera_object_utils import save_recognized_objects
import cv2

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
raw_images_dir = os.path.join(BASE_DIR, dt_string, 'raw')
cv2_images_dir = os.path.join(BASE_DIR, dt_string, 'cv2')
seg_images_dir = os.path.join(BASE_DIR, dt_string, 'seg')
rec_objects_dir = os.path.join(BASE_DIR, dt_string, 'rec_objects')

os.makedirs(raw_images_dir)
os.makedirs(cv2_images_dir)
os.makedirs(seg_images_dir)
os.makedirs(rec_objects_dir)

image_number = 0

cm.recognitionEnable(TIME_STEP)
cm.enableRecognitionSegmentation()

while robot.step(TIME_STEP) != -1:
    image_number += 1
    cm.saveImage(f"{os.path.join(raw_images_dir, str(image_number))}.jpg", 70)
    cm.saveRecognitionSegmentationImage(f"{os.path.join(seg_images_dir, str(image_number))}.jpg", 70)
    recognized_objects = cm.getRecognitionObjects()
    save_recognized_objects(recognized_objects, file_path=f"{os.path.join(rec_objects_dir, str(image_number))}.json")
    # image_array = np.asarray(cm.getImageArray())
    # print(image_array)
    # # cv2.imwrite(f"{os.path.join(cv2_images_dir, str(image_number))}.png", image_array)

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
