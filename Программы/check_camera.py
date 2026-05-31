#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class CameraChecker:
    def __init__(self):
        rospy.init_node("camera_checker_node")

        self.bridge = CvBridge()
        self.frame_count = 0

        rospy.Subscriber(
            "/robot_camera/image_raw",
            Image,
            self.image_callback
        )

        rospy.loginfo("Camera checker started")
        rospy.loginfo("Waiting for images from /robot_camera/image_raw...")

        rospy.spin()

    def image_callback(self, msg):
        self.frame_count += 1

        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        height, width, channels = frame.shape

        rospy.loginfo(
            "Frame %d received: width=%d height=%d channels=%d",
            self.frame_count,
            width,
            height,
            channels
        )

        cv2.imshow("Robot camera image", frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    try:
        CameraChecker()
    except rospy.ROSInterruptException:
        pass
