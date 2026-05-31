#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist


def move(pub, linear_x, angular_z, time_sec):
    cmd = Twist()
    cmd.linear.x = linear_x
    cmd.angular.z = angular_z

    rate = rospy.Rate(10)
    start = rospy.Time.now()

    while not rospy.is_shutdown():
        if (rospy.Time.now() - start).to_sec() >= time_sec:
            break
        pub.publish(cmd)
        rate.sleep()


def stop(pub):
    cmd = Twist()
    rate = rospy.Rate(10)

    for i in range(10):
        pub.publish(cmd)
        rate.sleep()


def main():
    rospy.init_node("move_robot_node")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    rospy.sleep(1)

    # 1. Едет прямо
    rospy.loginfo("Едем прямо")
    move(pub, 0.2, 0.0, 3.0)
    stop(pub)
    rospy.sleep(1)

    # 2. Поворот налево примерно на 90 градусов
    rospy.loginfo("Поворот налево на 90 градусов")
    move(pub, 0.0, 0.6, 2.6)
    stop(pub)
    rospy.sleep(1)

    # 3. Поворот направо примерно на 90 градусов
    rospy.loginfo("Поворот направо на 90 градусов")
    move(pub, 0.0, -0.6, 2.6)
    stop(pub)
    rospy.sleep(1)

    # 4. Едет назад
    rospy.loginfo("Едем назад")
    move(pub, -0.2, 0.0, 3.0)
    stop(pub)

    rospy.loginfo("Программа завершена")


if __name__ == "__main__":
    main()