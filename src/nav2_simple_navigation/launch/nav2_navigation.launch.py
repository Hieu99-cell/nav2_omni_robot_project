import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml
def generate_launch_description():
    # 1. Khai báo các đường dẫn (Sửa tên package của bạn ở đây)
    my_nav_pkg = get_package_share_directory('nav2_simple_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    bt_xml_path = os.path.join(my_nav_pkg, 'config', 'navigate_to_pose_w_replanning_and_recovery.xml')
    # 2. Các cấu hình tham số
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Trỏ thẳng đến map bệnh viện bạn vừa quét
    map_dir = LaunchConfiguration('map', 
        default=os.path.join(my_nav_pkg, 'config', 'hospital_map.yaml'))

    # Trỏ đến file params đã chỉnh sửa cho HV-100
    param_file_path = os.path.join(my_nav_pkg, 'config', 'nav2_params1.yaml')

    param_dir = LaunchConfiguration('params_file')
    param_substitutions = {
        'default_nav_to_pose_bt_xml': bt_xml_path,
        'default_nav_through_poses_bt_xml': bt_xml_path,
        'use_sim_time': use_sim_time
    }

    configured_params = RewrittenYaml(
        source_file=param_file_path,
        root_key='',
        param_rewrites=param_substitutions,
        convert_types=True
    )
    # Khai báo Node Relay để tự động nối dây
    relay_node = Node(
        package='topic_tools',
        executable='relay',
        name='relay_cmd_vel',
        arguments=['/cmd_vel_smoothed', '/mobile_base_controller/reference'],
        parameters=[{'use_sim_time': True}]
    )
   
    return LaunchDescription([
        DeclareLaunchArgument('map', default_value=map_dir),
        DeclareLaunchArgument('params_file', default_value=param_file_path),
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # Gọi lõi Nav2
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
            launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': configured_params,
                'autostart': 'true'}.items(),
        ),
        # Node(
        #     package='nav2_bt_navigator',
        #     executable='bt_navigator',
        #     name='bt_navigator',
        #     output='screen',
        #     parameters=[
        #         param_file_path, # Load file yaml trước
        #         {
        #             'default_nav_to_pose_bt_xml': bt_xml_path,
        #             'default_nav_through_poses_bt_xml': bt_xml_path,
        #             'use_sim_time': use_sim_time
        #         } # Đè đường dẫn thực tế lên sau
        #     ]
        # ),
        # Chạy RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
        relay_node,
        
        
    ])