#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import yaml
import os
import re
from ament_index_python.packages import get_package_share_directory
from .ga import calculate_optimal_route 

class TaskManager(Node):
    def __init__(self):
        super().__init__('task_manager_node')
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST, depth=1
        )
        self.curr_x, self.curr_y = None, None
        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.pose_callback, qos_profile)

    def pose_callback(self, msg):
        self.curr_x = msg.pose.pose.position.x
        self.curr_y = msg.pose.pose.position.y

def main():
    rclpy.init()
    task_node = TaskManager()
    navigator = BasicNavigator()

    # 1. Đọc file rooms.yaml
    try:
        package_share_dir = get_package_share_directory('nav2_simple_navigation')
        yaml_file_path = os.path.join(package_share_dir, 'config', 'rooms.yaml')
        with open(yaml_file_path, 'r') as f:
            rooms_data = yaml.safe_load(f)['rooms']
    except Exception as e:
        task_node.get_logger().error(f"Lỗi đọc file YAML: {e}")
        return

    print("--- Đang đợi AMCL xác định vị trí robot... ---")
    while rclpy.ok() and task_node.curr_x is None:
        rclpy.spin_once(task_node, timeout_sec=0.1)

    # 2. Khởi tạo danh sách điểm đi
    start_pos = [task_node.curr_x, task_node.curr_y]
    all_points = [start_pos]
    point_labels = ["Vị trí hiện tại"]

    # 3. Nhập số phòng (Xử lý chuỗi thông minh cho 20 phòng)
    user_input = input("Nhập danh sách số phòng (ví dụ: 20, 1, 14): ")
    # Dùng regex để chỉ lấy số, bỏ qua dấu phẩy, khoảng trắng, ký tự lạ
    room_numbers = re.findall(r'\d+', user_input)

    for num in room_numbers:
        room_key = f'room{num}'
        if room_key in rooms_data:
            room = rooms_data[room_key]
            all_points.append([room['x'], room['y']])
            point_labels.append(room_key)
            print(f"✅ Đã thêm {room_key} vào danh sách chờ.")
        else:
            print(f"⚠️ Cảnh báo: Không tìm thấy {room_key} trong file YAML!")

    if len(all_points) < 2:
        print("❌ Không có điểm đến hợp lệ. Kết thúc.")
        return

    # 4. Chạy GA (Với tham số mạnh cho 20 phòng)
    print(f"--- GA đang tính toán lộ trình tối ưu cho {len(all_points)-1} phòng ---")
    # Chúng ta tăng pop_size và generations trực tiếp tại đây
    optimal_indices = calculate_optimal_route(all_points, pop_size=300, num_generations=1000, return_to_depot=False)
    
    print("\n🚩 Lộ trình tối ưu tìm được:")
    for idx in optimal_indices:
        print(f" -> {point_labels[idx]}")

    # 5. Gửi mục tiêu cho Nav2
    goal_poses = []
    # Quan trọng: optimal_indices[0] luôn là 0 (vị trí hiện tại), ta bắt đầu từ index 1
    for i in range(1, len(optimal_indices)):
        idx = optimal_indices[i]
        pos = all_points[idx]
        
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = float(pos[0])
        goal_pose.pose.position.y = float(pos[1])
        # Bạn có thể lấy thêm Yaw từ YAML nếu muốn robot xoay đúng hướng phòng
        goal_pose.pose.orientation.w = 1.0 
        goal_poses.append(goal_pose)

    print("\n🚀 Robot bắt đầu di chuyển...")
    navigator.followWaypoints(goal_poses)

    while not navigator.isTaskComplete():
        # In ra feedback nếu cần (ví dụ waypoint hiện tại)
        feedback = navigator.getFeedback()
        # rclpy.spin_once(task_node, timeout_sec=0.1)
        pass

    print("\n✅ Đã hoàn thành toàn bộ lộ trình!")
    rclpy.shutdown()

if __name__ == '__main__':
    main()