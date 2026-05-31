#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge


class YellowCubeFinder:
    def init(self):
        rospy.init_node("yellow_cube_finder")

        self.bridge = CvBridge()

        self.cmd_pub = rospy.Publisher(
            "/cmd_vel",
            Twist,
            queue_size=10
        )

        rospy.Subscriber(
            "/robot_camera/image_raw",
            Image,
            self.image_callback
        )

        self.image_width = 640

        rospy.loginfo("Yellow cube finder started")
        rospy.spin()

    def publish_stop(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_pub.publish(cmd)

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([20, 80, 80])
        upper_yellow = np.array([35, 255, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        yellow_area = cv2.countNonZero(mask)

        moments = cv2.moments(mask)

        cmd = Twist()

        if yellow_area > 45000:
            rospy.loginfo("Yellow cube is close. STOP. area=%d", yellow_area)
            self.publish_stop()
            return

        if moments["m00"] > 5000:
            cx = int(moments["m10"] / moments["m00"])

            error = cx - self.image_width / 2

            cmd.angular.z = -0.003 * error

            if abs(error) < 60:
                cmd.linear.x = 0.12
            else:
                cmd.linear.x = 0.0

            rospy.loginfo(
                "Yellow cube found. cx=%d error=%.1f area=%d",
                cx,
                error,
                yellow_area
            )

        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.25

            rospy.loginfo("Searching yellow cube...")

        self.cmd_pub.publish(cmd)


if name == "main":
    try:
        YellowCubeFinder()
    except rospy.ROSInterruptException:
        pass