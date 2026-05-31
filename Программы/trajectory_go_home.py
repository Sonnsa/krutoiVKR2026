#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class RobotTrajectoryHome:
    def __init__(self):
        rospy.init_node("trajectory_go_home_node")

        self.cmd_pub = rospy.Publisher(
            "/cmd_vel",
            Twist,
            queue_size=10
        )

        rospy.Subscriber(
            "/odom",
            Odometry,
            self.odom_callback
        )

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.start_x = None
        self.start_y = None
        self.start_theta = None

        rospy.sleep(2.0)

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation

        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)

        self.theta = math.atan2(siny_cosp, cosy_cosp)

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi

        while angle < -math.pi:
            angle += 2.0 * math.pi

        return angle

    def stop(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0

        rate = rospy.Rate(10)

        for i in range(10):
            self.cmd_pub.publish(cmd)
            rate.sleep()

    def move_time(self, linear_x, angular_z, duration):
        cmd = Twist()
        cmd.linear.x = linear_x
        cmd.angular.z = angular_z

        rate = rospy.Rate(10)
        start_time = rospy.Time.now()

        while not rospy.is_shutdown():
            elapsed = (rospy.Time.now() - start_time).to_sec()

            if elapsed >= duration:
                break

            self.cmd_pub.publish(cmd)
            rate.sleep()

        self.stop()

    def save_start_position(self):
        self.start_x = self.x
        self.start_y = self.y
        self.start_theta = self.theta

        rospy.loginfo(
            "Start position saved: x=%.3f y=%.3f theta=%.3f",
            self.start_x,
            self.start_y,
            self.start_theta
        )

    def go_home(self):
        rospy.loginfo("Going home by odometry")

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            dx = self.start_x - self.x
            dy = self.start_y - self.y

            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 0.08:
                rospy.loginfo("Home point reached")
                self.stop()
                break

            target_angle = math.atan2(dy, dx)
            angle_error = self.normalize_angle(target_angle - self.theta)

            cmd = Twist()

            if abs(angle_error) > 0.15:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.8 * angle_error
            else:
                cmd.linear.x = 0.18
                cmd.angular.z = 0.8 * angle_error

            self.cmd_pub.publish(cmd)

            rospy.loginfo(
                "Going home: distance=%.3f angle_error=%.3f",
                distance,
                angle_error
            )

            rate.sleep()

        self.stop()

    def align_to_start_heading(self):
        rospy.loginfo("Aligning to start orientation")

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            angle_error = self.normalize_angle(
                self.start_theta - self.theta
            )

            if abs(angle_error) < 0.03:
                rospy.loginfo("Start orientation restored")
                self.stop()
                break

            cmd = Twist()
            cmd.linear.x = 0.0
            cmd.angular.z = 1.0 * angle_error

            self.cmd_pub.publish(cmd)

            rospy.loginfo(
                "Aligning: angle_error=%.3f",
                angle_error
            )

            rate.sleep()

        self.stop()

    def run(self):
        self.save_start_position()

        rospy.loginfo("Step 1: move forward")
        self.move_time(0.2, 0.0, 3.0)
        rospy.sleep(1.0)

        rospy.loginfo("Step 2: turn left 90 degrees")
        self.move_time(0.0, 0.6, 2.6)
        rospy.sleep(1.0)

        rospy.loginfo("Step 3: turn right 90 degrees")
        self.move_time(0.0, -0.6, 2.6)
        rospy.sleep(1.0)

        rospy.loginfo("Step 4: move along arc to the right")
        self.move_time(0.15, -0.35, 4.0)
        rospy.sleep(1.0)

        rospy.loginfo("Step 5: move along arc to the left")
        self.move_time(0.15, 0.35, 4.0)
        rospy.sleep(1.0)

        rospy.loginfo("Step 6: move backward")
        self.move_time(-0.2, 0.0, 3.0)
        rospy.sleep(1.0)

        rospy.loginfo("Step 7: return to start position")
        self.go_home()
        rospy.sleep(1.0)

        rospy.loginfo("Step 8: restore start orientation")
        self.align_to_start_heading()

        rospy.loginfo("Program finished")


if __name__ == "__main__":
    try:
        robot = RobotTrajectoryHome()
        robot.run()
    except rospy.ROSInterruptException:
        pass
