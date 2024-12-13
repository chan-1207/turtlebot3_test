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
            parameters=[{'queue_size': 20}],
            # remappings=[
            #     ('image', 'image'),
            #     ('image_rect', 'image_rect')
            # ]
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
    return LaunchDescription([

        Node(
            package='image_transport',
            executable='republish',
            name='republish',
            output='screen',
            #parameters=['compressed','raw'],
            arguments=[
                'compressed',            # 입력 이미지 형식: 압축된 이미지 (CompressedImage)
                'raw'                    # 출력 이미지 형식: 원시 이미지 (Image)
            ],
            remappings=[
                ('in/compressed', '/camera/image_raw/compressed'), 
                ('out', '/camera/image')]
        ),
        # 그룹 안의 토픽 도구 릴레이 노드
        Node(
            package='topic_tools',
            executable='relay',
            name='relay_camera_info',
            output='screen',
            arguments=['/camera/camera_info', '/camera/camera_info']
        ),
        
        # 이미지 보정 노드
        # Node(
        #     package='image_proc',
        #     executable='image_proc',
        #     namespace='camera',
        #     #name='image_proc',
        #     output='screen',
        #     parameters=[{'queue_size': 20}],
        #     remappings=[('image_raw', 'image')],
        #     arguments=['--ros-args --remap _approximate_sync:=true']
        # ),
        ComposableNodeContainer(
        name='image_proc_container',
        namespace='camera',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=composable_nodes,
        )

    ])
