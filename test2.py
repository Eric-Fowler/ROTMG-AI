import dxcam

# install OpenCV using `pip install dxcam[cv2]` command.
import cv2
import numpy as np
import matplotlib.pyplot as plt

import mouse
import keyboard

mouse_events = []
keyboard_events = []

TOP = 0
LEFT = 0
RIGHT = 1920
BOTTOM = 1080
region = (LEFT, TOP, RIGHT, BOTTOM)
title = "[DXcam] Capture benchmark"


target_fps = 60
time = 2
scale = 4
nw,nh = (int(RIGHT/scale),int(BOTTOM/scale))

camera = dxcam.create(output_idx=0, output_color="RGB")
images = []
camera.start(target_fps=target_fps, video_mode=True)

keyboard_list = ["w","a","s","d","q","e","r"]
keyboard_inst = [0,0,0,0,0,0,0]

for i in range(target_fps*time):
    frame = camera.get_latest_frame()
    small = cv2.resize(frame,(nw,nh))

    images.append(small)
    mouse_events.append(mouse.get_position())
    for i, keyval in enumerate(keyboard_list):
        if keyboard.is_pressed(keyval):
            keyboard_inst[i] = 1
        else:
            keyboard_inst[i] = 0
    keyboard_events.append(keyboard_inst)
camera.stop()

print(mouse_events[-1])
print(keyboard_events[-1])
plt.figure()
plt.imshow(images[-1])
plt.show()