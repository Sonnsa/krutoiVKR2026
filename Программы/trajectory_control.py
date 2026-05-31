#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState


def publish_motion(pub, linear_x, angular_z, duration):
    cmd = Twist()
    cmd.linear.x = linear_x
    cmd.angular.z = angular_z

    rate = rospy.Rate(10)
    start_time = rospy.Time.now()

    while not rospy.is_shutdown():
        elapsed = (rospy.Time.now() - start_time).to_sec()

        if elapsed >= duration:
            break

        pub.publish(cmd)
        rate.sleep()


def stop_robot(pub):
    cmd = Twist()
    cmd.linear.x = 0.0
    cmd.angular.z = 0.0

    rate = rospy.Rate(10)

    for i in range(10):
        pub.publish(cmd)
        rate.sleep()


def reset_robot_position():
    rospy.wait_for_service("/gazebo/set_model_state")

    reset_service = rospy.ServiceProxy(
        "/gazebo/set_model_state",
        SetModelState
    )

    state = ModelState()
    state.model_name = "my_robot"

    state.pose.position.x = 0.0
    state.pose.position.y = 0.0
    state.pose.position.z = 0.12

    state.pose.orientation.x = 0.0
    state.pose.orientation.y = 0.0
    state.pose.orientation.z = 0.0
    state.pose.orientation.w = 1.0

    state.twist.linear.x = 0.0
    state.twist.linear.y = 0.0
    state.twist.linear.z = 0.0

    state.twist.angular.x = 0.0
    state.twist.angular.y = 0.0
    state.twist.angular.z = 0.0

    state.reference_frame = "world"

    response = reset_service(state)

    if response.success:
        rospy.loginfo("Robot returned to start position")
    else:
        rospy.logwarn("Failed to return robot to start position")


def main():
    rospy.init_node("trajectory_control_node")

    pub = rospy.Publisher(
        "/cmd_vel",
        Twist,
        queue_size=10
    )

    rospy.sleep(1.0)

    rospy.loginfo("Step 1: move forward")
    publish_motion(pub, 0.2, 0.0, 3.0)
    stop_robot(pub)
    rospy.sleep(1.0)

    rospy.loginfo("Step 2: turn left 90 degrees")
    publish_motion(pub, 0.0, 0.6, 2.6)
    stop_robot(pub)
    rospy.sleep(1.0)

    rospy.loginfo("Step 3: turn right 90 degrees")
    publish_motion(pub, 0.0, -0.6, 2.6)
    stop_robot(pub)
    rospy.sleep(1.0)

    rospy.loginfo("Step 4: move along arc to the right")
    publish_motion(pub, 0.15, -0.35, 4.0)
    stop_robot(pub)
    rospy.sleep(1.0)

    rospy.loginfo("Step 5: move along arc to the left")
    publish_motion(pub, 0.15, 0.35, 4.0)
    stop_robot(pub)
    rospy.sleep(1.0)

    rospy.loginfo("Step 6: move backward")
    publish_motion(pub, -0.2, 0.0, 3.0)
    stop_robot(pub)
    rospy.sleep(1.0)

    rospy.loginfo("Step 7: return to start position")
    reset_robot_position()

    rospy.loginfo("Trajectory program finished")


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
