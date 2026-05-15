import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('humanoid_head')

    urdf_path = os.path.join(pkg_share, 'urdf', 'humanoid_head.urdf')
    with open(urdf_path, 'r') as f:
        robot_desc = f.read()

    world_path = os.path.join(pkg_share, 'worlds', 'empty.world')

    # 1. Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('gazebo_ros'),
            '/launch/gazebo.launch.py'
        ]),
        launch_arguments={'world': world_path}.items(),
    )

    # 2. Robot state publisher
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
    )

    # 3. Spawn head model
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'humanoid_head', '-file', urdf_path,
                   '-x', '0', '-y', '0', '-z', '0.05'],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    # 4. Expression engine (PD controller + state machine)
    expression_engine = Node(
        package='humanoid_head',
        executable='expression_engine',
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    # Stagger startup
    delayed_rsp = TimerAction(period=2.0, actions=[robot_state_pub])
    delayed_spawn = TimerAction(period=3.0, actions=[spawn_entity])
    delayed_engine = TimerAction(period=5.0, actions=[expression_engine])

    return LaunchDescription([
        gazebo,
        delayed_rsp,
        delayed_spawn,
        delayed_engine,
    ])
