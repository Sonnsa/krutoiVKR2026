#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D


pose_pub = None


def quaternion_to_yaw(q):
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)

    yaw = math.atan2(siny_cosp, cosy_cosp)

    return yaw


def odom_callback(msg):
    global pose_pub

    pose2d = Pose2D()

    pose2d.x = msg.pose.pose.position.x
    pose2d.y = msg.pose.pose.position.y
    pose2d.theta = quaternion_to_yaw(msg.pose.pose.orientation)

    pose_pub.publish(pose2d)

    rospy.loginfo(
        "x: %.3f, y: %.3f, theta: %.3f",
        pose2d.x,
        pose2d.y,
        pose2d.theta
    )


def main():
    global pose_pub

    rospy.init_node("odom_pose2d_node")

    pose_pub = rospy.Publisher(
        "/odom_pose2d",
        Pose2D,
        queue_size=10
    )

    rospy.Subscriber(
        "/odom",
        Odometry,
        odom_callback
    )

    rospy.loginfo("odom_pose2d node started")

    rospy.spin()


if name == "main":
    main()