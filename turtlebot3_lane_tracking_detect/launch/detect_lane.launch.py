from launch import LaunchDescription
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch argument
    calibration_mode_arg = DeclareLaunchArgument(
        'calibration_mode',
        default_value='False',
        description='Mode type [calibration, action]'
    )
    calibration_mode=LaunchConfiguration('calibration_mode')

    detect_param = os.path.join(
        get_package_share_directory('turtlebot3_lane_tracking_detect'),
        'param',
        'lane',
        'lane.yaml'
        )
    

    
    # Define the node
    detect_lane_node = Node(
        package='turtlebot3_lane_tracking_detect',
        executable='detect_lane.py',
        name='detect_lane',
        output='screen',
        parameters=[
            {'is_detection_calibration_mode': calibration_mode},
            detect_param
        ],
        remappings=[
            ('/detect/image_input', '/camera/image_projected_compensated'),
            ('/detect/image_input/compressed', '/camera/image_projected_compensated/compressed'),
            ('/detect/image_output', '/detect/image_lane'),
            ('/detect/image_output/compressed', '/detect/image_lane/compressed'),
            ('/detect/image_output_sub1', '/detect/image_white_lane_marker'),
            ('/detect/image_output_sub1/compressed', '/detect/image_white_lane_marker/compressed'),
            ('/detect/image_output_sub2', '/detect/image_yellow_lane_marker'),
            ('/detect/image_output_sub2/compressed', '/detect/image_yellow_lane_marker/compressed'),
        ]
    )

    # Launch description
    return LaunchDescription([
        calibration_mode_arg,
        detect_lane_node,
    ])