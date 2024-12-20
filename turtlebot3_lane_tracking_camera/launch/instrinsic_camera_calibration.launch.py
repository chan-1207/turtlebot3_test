from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():

    composable_nodes = [
        ComposableNode(
            package='image_proc',
            plugin='image_proc::RectifyNode',
            name='rectify_node',
            namespace='camera',
            parameters=[{'queue_size': 20}]
        ),

        ComposableNode(
            package='image_proc',
            plugin='image_proc::DebayerNode',
            name='debayer_node',
            namespace='camera',
            remappings=[
                ('image_raw', 'image_rect'),
                ('image_color/compressed', 'image_rect_color/compressed')
            ]
        )
    ]

    republish_node = Node(
        package='image_transport',
        executable='republish',
        name='republish',
        output='screen',
        arguments=[
            'compressed',
            'raw'],
        remappings=[
            ('in/compressed',
                '/camera/image_raw/compressed'),
            ('out',
                '/camera/image')]
    )

    relay_node = Node(
        package='topic_tools',
        executable='relay',
        name='relay_camera_info',
        output='screen',
        arguments=['/camera/camera_info', '/camera/camera_info']
    )

    image_proc_container = ComposableNodeContainer(
        name='image_proc_container',
        namespace='camera',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=composable_nodes,
    )

    return LaunchDescription([
        republish_node,
        relay_node,
        image_proc_container
    ])
