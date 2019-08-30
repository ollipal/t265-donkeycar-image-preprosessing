import sys
sys.path.append("/usr/local/lib")
import time
import pyrealsense2 as rs
import numpy as np
import cv2
from donkeycar.parts.camera import BaseCamera


class RealSenseCamera(BaseCamera):
    def __init__(self, resolution=(848, 800), framerate=20):
        cfg = rs.config()
        self.pipeline = rs.pipeline()

        cfg.enable_stream(rs.stream.fisheye, 1) # Left camera
        cfg.enable_stream(rs.stream.fisheye, 2) # Right camera

        self.pipeline.start(cfg)
        self.frame = None
        self.on = True

        print('RealSense Camera loaded... warming up camera')
        time.sleep(2)

    def run(self):
        # get both camera frames
        left = frames.get_fisheye_frame(1)
        right = frames.get_fisheye_frame(2)

        # crop only the necessary parts
        left = left[352:592, 21:831]
        right = right[352:592, 21:831]

        # combine to a single frame
        frame = np.concatenate((left, right), axis=0)

        # resize frame
        frame = cv2.resize(frame, (230, 180))
        
        # blur and threshold frame
        # blurring redused noise and unwanted reflections from the image
        frame = cv2.blur(frame, (2, 2))
        _, frame = cv2.threshold(frame, 210, 255, cv2.THRESH_BINARY)

        return frame

    def update(self):
        while True:
            self.frame = self.run()

            if not self.on:
                break

    def shutdown(self):
        self.on = False
        print('Stopping RealSense Camera')
        self.pipeline.stop()
