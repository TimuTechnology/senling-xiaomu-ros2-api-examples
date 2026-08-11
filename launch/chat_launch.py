from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('root_dir', default_value='/root'),
        DeclareLaunchArgument('language', default_value='zh-Hans'),
        Node(
            package='example',
            namespace='tmmini',
            executable='chat',
            name='chat',
            parameters=[{
                'root_dir': LaunchConfiguration('root_dir'),
                'language': LaunchConfiguration('language'),
            }]
        ),
    ])
