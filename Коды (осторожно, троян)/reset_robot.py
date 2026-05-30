import rospy

from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState


def main():
    rospy.init_node("reset_robot_node")

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
        rospy.logwarn("Failed to reset robot position")


if name == "main":
    try:
        main()
    except rospy.ROSInterruptException:
        pass