import dxcam

# install OpenCV using `pip install dxcam[cv2]` command.
import cv2
import numpy as np
import matplotlib.pyplot as plt

TOP = 0
LEFT = 0
RIGHT = 1920
BOTTOM = 1080
region = (LEFT, TOP, RIGHT, BOTTOM)
title = "[DXcam] Capture benchmark"

scale = 1
# l,w = (int(RIGHT/scale),int(BOTTOM/scale))


target_fps = 30
time = 2
scale = 1
nw,nh = (int(RIGHT/scale),int(BOTTOM/scale))
camera = dxcam.create(output_idx=0, output_color="RGB")
images = []
camera.start(target_fps=target_fps, video_mode=True)
# writer = cv2.VideoWriter(
#     "video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), target_fps, (nw, nh)
# )
for i in range(target_fps*time):
    frame = camera.get_latest_frame()
    small = cv2.resize(frame,(nw,nh))
    images.append(small)
    # writer.write(small)
    # writer.write(camera.get_latest_frame())
camera.stop()
# writer.release()
print(np.shape(images))
plt.figure()
plt.imshow(frame)
plt.show()