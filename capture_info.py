import dxcam

# install OpenCV using `pip install dxcam[cv2]` command.
import cv2
import numpy as np
import matplotlib.pyplot as plt

import mouse
import keyboard

import os
import time


class CapInfo:
    def __init__(
        self, top=0, left=0, right=1920, bottom=1080, fps_target=60, scaling=1
    ):
        self.mouse_events = []
        self.keyboard_events = []
        self.images = []

        self.TOP = top
        self.LEFT = left
        self.RIGHT = right
        self.BOTTOM = bottom
        self.region = (self.LEFT, self.TOP, self.RIGHT, self.BOTTOM)

        self.scale = scaling
        self.nw, self.nh = (int(self.RIGHT / self.scale), int(self.BOTTOM / self.scale))

        self.target_fps = fps_target

        self.camera = dxcam.create(output_idx=0, output_color="RGB")
        self.keyboard_list = ["w", "a", "s", "d", "q", "e", "r"]
        self.keyboard_inst = [0, 0, 0, 0, 0, 0, 0]

        self.breakout = False

    def grab_data(self, duration=10, break_char="p"):
        self.time = duration
        self.cbreak = break_char
        for i in range(self.target_fps * self.time):
            self.frame = self.camera.get_latest_frame()
            self.small = cv2.resize(self.frame, (self.nw, self.nh))

            self.images.append(self.small)
            self.mouse_events.append(mouse.get_position())
            for i, keyval in enumerate(self.keyboard_list):
                if keyboard.is_pressed(keyval):
                    self.keyboard_inst[i] = 1
                else:
                    self.keyboard_inst[i] = 0
            self.keyboard_events.append(self.keyboard_inst)
            if keyboard.is_pressed(self.cbreak):
                self.breakout = True
                break

    def grab_until_p(self, break_char="p"):
        self.cbreak = break_char
        while True:
            self.frame = self.camera.get_latest_frame()
            self.small = cv2.resize(self.frame, (self.nw, self.nh))

            self.images.append(self.small)
            self.mouse_events.append(mouse.get_position())
            for i, keyval in enumerate(self.keyboard_list):
                if keyboard.is_pressed(keyval):
                    self.keyboard_inst[i] = 1
                else:
                    self.keyboard_inst[i] = 0
            self.keyboard_events.append(self.keyboard_inst)
            if keyboard.is_pressed(break_char):
                break

    def save_data(self, filepath="./Saved_Data"):
        self.save_path = filepath
        self.keyboard_mat = (
            filepath + "/" + str(self.nw) + "x" + str(self.nh) +"_"+str(self.target_fps)+"fps_keyboard.npy"
        )
        self.mouse_mat = (
            filepath + "/" + str(self.nw) + "x" + str(self.nh) +"_"+str(self.target_fps)+ "fps_mouse.npy"
        )
        self.image_mat = (
            filepath + "/" + str(self.nw) + "x" + str(self.nh) +"_"+str(self.target_fps)+ "fps_images.npy"
        )

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        try:
            self.save_keyboard = np.concatenate(
                np.loadtxt(self.keyboard_mat), self.keyboard_events
            )
            self.save_mouse = np.concatenate(
                np.loadtxt(self.mouse_mat), self.mouse_events
            )
            self.save_images = np.concatenate(np.loadtxt(self.image_mat), self.images)
        except:
            self.save_keyboard = self.keyboard_events
            self.save_mouse = self.mouse_events
            self.save_images = self.images
        np.save(self.keyboard_mat, self.save_keyboard)
        np.save(self.mouse_mat, self.save_mouse)
        np.save(self.image_mat, self.save_images)
        # self.clear_data()

    def clear_data(self):
        self.keyboard_events = []
        self.mouse_events = []
        self.images = []

    def indefinite_segments(self, runtime=10, break_char="p"):
        self.breakout = False
        self.start_time = time.time()
        while True:
            self.camera.start(target_fps=self.target_fps, video_mode=True)
            self.grab_data(runtime, break_char)
            self.save_data()
            self.clear_data()
            self.camera.stop()
            if self.breakout is True:
                print("Finished")
                break
        print("Runtime: " + str(time.time() - self.start_time) + " seconds")


capturer = CapInfo(top=0, left=0, right=1920, bottom=1080, fps_target=60, scaling=4)
capturer.indefinite_segments(10, "p")
