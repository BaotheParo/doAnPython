import pygame
import json
import os

class TimeSystem:
    def __init__(self, filename="time_data.json"):
        # Xác định đường dẫn thư mục data dựa trên file hiện tại
        save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
        # Nếu thư mục chưa tồn tại, tạo mới nó
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # Ghép đường dẫn thư mục với tên file lưu trữ
        self.save_file = os.path.join(save_dir, filename)
        
        self.day_duration = 50000  # Ban ngày = 50,000 ms
        self.night_duration = 10000  # Ban đêm = 20,000 ms
        self.day_length = self.day_duration + self.night_duration  # Tổng thời gian của ngày (70,000 ms)
        self.load_time_data()

    def load_time_data(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.current_day = data.get("current_day", 0)
                self.remaining_day_time = data.get("remaining_day_time", self.day_duration)
                self.is_day_state = data.get("is_day_state", True)
        else:
            self.current_day = 0
            self.remaining_day_time = self.day_duration  # Bắt đầu bằng ban ngày
            self.is_day_state = True

    def save_time_data(self):
        data = {
            "current_day": self.current_day,
            "remaining_day_time": self.remaining_day_time,
            "is_day_state": self.is_day_state
        }
        with open(self.save_file, "w") as f:
            json.dump(data, f)
        print(f"Thời gian đã được lưu vào {self.save_file}")

    def update(self, delta_time):
        self.remaining_day_time -= delta_time
        if self.remaining_day_time <= 0:
            if self.is_day_state:
                self.is_day_state = False
                self.remaining_day_time += self.night_duration
            else:
                self.is_day_state = True
                self.remaining_day_time += self.day_duration
                self.current_day += 1

    def is_day(self):
        return self.is_day_state

    def get_remaining_time(self):
        return self.remaining_day_time

    def get_time_of_day(self):
        return "Ngày" if self.is_day() else "Đêm"

    def format_time(self, milliseconds):
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
