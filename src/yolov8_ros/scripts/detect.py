#!/usr/bin/env python3

import rospy
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO

from sensor_msgs.msg import Image

class Detector:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')

        self.image_sub = rospy.Subscriber(
            "/usb_cam/image_raw", Image, self.callback, queue_size=1
        )

        self.bridge = CvBridge()


    def callback(self, data):
        im = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

        im = cv2.flip(im, 1)
        im0 = self.model([im])[0].plot()

        cv2.imshow('sample', im0)
        cv2.waitKey(3)

        
if __name__ == "__main__":


    rospy.init_node("yolov8", anonymous=True)
    detector = Detector()
    
    rospy.spin()