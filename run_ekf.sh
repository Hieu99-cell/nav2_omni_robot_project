#!/bin/bash
source env_config.sh
cd $MY_ROBOT_PATH
colcon build --packages-select nav2_simple_navigation
source install/setup.bash
ros2 launch nav2_simple_navigation ekf.launch.py | grep ERROR use_sim_time:=True