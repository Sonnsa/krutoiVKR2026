#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist


def move(pub, linear_x, angular_z, time_sec):
    cmd = Twist()
    cmd.linear.x = linear_x
    cmd.angular.z = angular_z

    rate = rospy.Rate(10)
    start_time = rospy.Time.now()

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()
        elapsed_time = (current_time - start_time).to_sec()

        if elapsed_time >= time_sec:
            break

        pub.publish(cmd)
        rate.sleep()


def stop(pub):
    cmd = Twist()
    cmd.linear.x = 0.0
    cmd.angular.z = 0.0

    rate = rospy.Rate(10)

    for i in range(10):
        pub.publish(cmd)
        rate.sleep()


def main():
    rospy.init_node("move_robot_node")

    pub = rospy.Publisher(
        "/cmd_vel",
        Twist,
        queue_size=10
    )

    rospy.sleep(1.0)

    rospy.loginfo("Robot moves forward")
    move(pub, 0.2, 0.0, 3.0)
    stop(pub)

    rospy.sleep(1.0)

    rospy.loginfo("Robot turns left 90 degrees")
    move(pub, 0.0, 0.6, 2.6)
    stop(pub)

    rospy.sleep(1.0)

    rospy.loginfo("Robot turns right 90 degrees")
    move(pub, 0.0, -0.6, 2.6)
    stop(pub)

    rospy.sleep(1.0)

    rospy.loginfo("Robot moves backward")
    move(pub, -0.2, 0.0, 3.0)
    stop(pub)

    rospy.loginfo("Program finished")


if name == "main":
    main()