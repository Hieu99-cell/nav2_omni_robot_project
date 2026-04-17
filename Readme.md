## Team Members

| Thành viên | MSSV |
|---|---|
| Lê Phan Công Hiếu | 23134017 |
| Nguyễn Quang Tùng | 23134062 |
| Vũ Trọng Tâm      | 23134051 | 
# Robot Omni Setup Guide

This guide provides instructions for setting up and running the Robot Omni simulation and navigation system.

## Prerequisites
- Ensure you have the necessary dependencies installed (e.g., Gazebo, ROS).
- Update paths to match your local environment.

## Configuration Steps

### 1. Update Gazebo Resource Path
Edit your `~/.bashrc` file to include the models directory:
```bash
nano ~/.bashrc
```
Add the following line at the end, replacing `<path_to_your_pkg>` with your actual package path:
```bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:<path_to_your_pkg>/models
```
Save the file, close the terminal, and open a new one.

### 2. Update URDF Configuration
In `urdf/omni_base.urdf`, modify the parameters path to your local configuration file:
```xml
<parameters>/path/to/your/robot_omni/config/configuration.yaml</parameters>
```

### 3. Update Environment Configuration
Edit `env_config.sh` to set the correct paths for your environment.

### 4. Grant Execute Permissions
Make all shell scripts executable:
```bash
chmod +x *.sh
```

## Running the System
Open separate terminals for each component and source the setup:

- **Terminal 1 (EKF)**:
  ```bash
  cd ~/nav2_omni_robot_project
  source install/setup.bash
  ./run_ekf.sh
  ```

- **Terminal 2 (Robot Omni)**:
  ```bash
  cd ~/nav2_omni_robot_project
  source install/setup.bash
  ./run_robot_omni.sh
  ```

- **Terminal 3 (Navigation)**:
  ```bash
  cd ~/nav2_omni_robot_project
  source install/setup.bash
  ./run_navigation.sh
  ```

- **Terminal 4 (Task)**:
  ```bash
  cd ~/nav2_omni_robot_project
  source install/setup.bash
  ./run_task.sh
  ```

For troubleshooting, refer to the project documentation or logs.
