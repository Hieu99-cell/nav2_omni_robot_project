source env_config.sh
cd $MY_ROBOT_PATH
source install/setup.bash
ros2 run nav2_map_server map_saver_cli -f src/nav2_simple_navigation/config/hospital_map
