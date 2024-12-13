import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    control_node = Node(
            package='turtlebot3_lane_tracking_drive',
            executable='control_lane.py',
            name='control_lane',
            output='screen',
            remappings=[
                ('/control/lane', '/detect/lane'),
                ('/control/cmd_vel', '/cmd_vel')
            ]
        )
    return LaunchDescription([
        control_node
    ])