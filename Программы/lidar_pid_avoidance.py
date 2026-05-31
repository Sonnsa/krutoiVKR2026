#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class LidarPIDAvoidance:
    def __init__(self):
        rospy.init_node("lidar_pid_avoidance_node")

        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        rospy.Subscriber("/scan", LaserScan, self.scan_callback)

        self.safe_distance = 0.75

        rospy.loginfo("Lidar avoidance by angle sectors started")
        rospy.spin()

    def get_sector_min(self, msg, angle_min_deg, angle_max_deg):
        result = []

        angle_min_rad = math.radians(angle_min_deg)
        angle_max_rad = math.radians(angle_max_deg)

        for i, r in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment

            if angle_min_rad <= angle <= angle_max_rad:
                if not math.isnan(r) and not math.isinf(r) and r > 0.05:
                    result.append(r)

        if len(result) == 0:
            return msg.range_max

        return min(result)

    def stop(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)

    def scan_callback(self, msg):
        # ВАЖНО:
        # 0 градусов — направление вперед
        # +90 градусов — слева
        # -90 градусов — справа

        front = self.get_sector_min(msg, -20, 20)
        left = self.get_sector_min(msg, 40, 100)
        right = self.get_sector_min(msg, -100, -40)

        cmd = Twist()

        if front > self.safe_distance:
            cmd.linear.x = 0.14
            cmd.angular.z = 0.0

            rospy.loginfo(
                "CLEAR: front=%.2f left=%.2f right=%.2f",
                front, left, right
            )

        else:
            cmd.linear.x = 0.02

            if left > right:
                cmd.angular.z = 0.65
                rospy.loginfo(
                    "OBSTACLE: turn LEFT front=%.2f left=%.2f right=%.2f",
                    front, left, right
                )
            else:
                cmd.angular.z = -0.65
                rospy.loginfo(
                    "OBSTACLE: turn RIGHT front=%.2f left=%.2f right=%.2f",
                    front, left, right
                )

        self.cmd_pub.publish(cmd)


if __name__ == "__main__":
    try:
        LidarPIDAvoidance()
    except rospy.ROSInterruptException:
        pass
