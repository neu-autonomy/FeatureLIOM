#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_share = get_package_share_directory('FeatureLIOM')
    default_params_file_path = os.path.join(pkg_share, 'config', 'params.yaml')

    args = [
        DeclareLaunchArgument(
            'pcd_topic',
            default_value='/dliom/odom_node/compress',
            description='Input PCD topic name'
        ),
        DeclareLaunchArgument(
            'downsampled_topic',
            default_value='/PointRec/descriptor_cloud',
            description='Output downsampled topic name'
        ),
        DeclareLaunchArgument(
            'params_file',
            default_value=default_params_file_path,
            description='Path to node parameter file'
        ),
    ]

    pcd_topic = LaunchConfiguration('pcd_topic')
    downsampled_topic = LaunchConfiguration('downsampled_topic')
    params_file = LaunchConfiguration('params_file')

    keypoint_node = Node(
        package='FeatureLIOM',
        executable='keypoint_node',
        name='keypoint_node',
        output='screen',
        parameters=[params_file],   
        arguments=[
            '--pcd_topic', pcd_topic,               
            '--downsampled_topic', downsampled_topic
        ],
        remappings=[
            ('/dliom/odom_node/compress', pcd_topic),            
            ('/PointRec/descriptor_cloud', downsampled_topic)
        ],
    )

    return LaunchDescription(args + [keypoint_node])