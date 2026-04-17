source env_config.sh
cd $MY_ROBOT_PATH
colcon build --packages-select robot_omni
cd $MY_ROBOT_PATH
source install/setup.bash
ros2 launch robot_omni hopistal_gazebo_control.launch.py use_sim_time:=True