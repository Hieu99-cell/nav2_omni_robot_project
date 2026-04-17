source env_config.sh
cd $MY_ROBOT_PATH
colcon build --packages-select nav2_simple_navigation
source install/setup.bash
ros2 run nav2_simple_navigation task_manager