#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class LidarAvoidance:
    def __init__(self):
        rospy.init_node("lidar_avoidance_node")

        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        rospy.Subscriber("/scan", LaserScan, self.scan_callback)

        self.front_distance = 10.0
        self.left_distance = 10.0
        self.right_distance = 10.0

        self.safe_distance = 0.55

        rospy.loginfo("Lidar obstacle avoidance started")
        rospy.spin()

    def get_min_range(self, ranges, start_index, end_index):
        selected_ranges = ranges[start_index:end_index]

        valid_ranges = []

        for value in selected_ranges:
            if not math.isnan(value) and not math.isinf(value):
                if value > 0.05:
                    valid_ranges.append(value)

        if len(valid_ranges) == 0:
            return 10.0

        return min(valid_ranges)

    def scan_callback(self, msg):
        ranges = list(msg.ranges)
        n = len(ranges)

        # Для 360 градусов:
        # вперед примерно около 0 градусов
        # слева около +90 градусов
        # справа около -90 градусов

        front_1 = self.get_min_range(ranges, 0, 30)
        front_2 = self.get_min_range(ranges, n - 30, n)
        self.front_distance = min(front_1, front_2)

        self.left_distance = self.get_min_range(ranges, int(n * 0.20), int(n * 0.40))
        self.right_distance = self.get_min_range(ranges, int(n * 0.60), int(n * 0.80))

        cmd = Twist()

        if self.front_distance > self.safe_distance:
            cmd.linear.x = 0.18
            cmd.angular.z = 0.0

            rospy.loginfo(
                "Path clear. front=%.2f left=%.2f right=%.2f",
                self.front_distance,
                self.left_distance,
                self.right_distance
            )

        else:
            cmd.linear.x = 0.0

            if self.left_distance > self.right_distance:
                cmd.angular.z = 0.45
                rospy.loginfo(
                    "Obstacle ahead. Turning left. front=%.2f left=%.2f right=%.2f",
                    self.front_distance,
                    self.left_distance,
                    self.right_distance
                )
            else:
                cmd.angular.z = -0.45
                rospy.loginfo(
                    "Obstacle ahead. Turning right. front=%.2f left=%.2f right=%.2f",
                    self.front_distance,
                    self.left_distance,
                    self.right_distance
                )

        self.cmd_pub.publish(cmd)


if __name__ == "__main__":
    try:
        LidarAvoidance()
    except rospy.ROSInterruptException:
        pass
