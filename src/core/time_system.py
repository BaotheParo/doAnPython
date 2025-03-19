import pygame
import json
import os

class TimeSystem:
    def __init__(self, save_file="D:\\ĐHSG\\Python\\Project\\doAnPython\\src\\core\\time_data.json"):
        self.save_file = save_file
        self.day_duration = 50000  # Ban ngày = 5 phút = 300,000 ms
        self.night_duration = 20000  # Ban đêm = 2 phút = 120,000 ms
        self.day_length = self.day_duration + self.night_duration  # 7 phút
        self.load_time_data()

    def load_time_data(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.current_day = data.get("current_day", 0)
                self.remaining_day_time = data.get("remaining_day_time", self.day_duration)  # Mặc định là ban ngày
                self.is_day_state = data.get("is_day_state", True)
        else:
            self.current_day = 0
            self.remaining_day_time = self.day_duration  # Bắt đầu bằng ngày
            self.is_day_state = True

    def save_time_data(self):
        data = {
            "current_day": self.current_day,
            "remaining_day_time": self.remaining_day_time,
            "is_day_state": self.is_day_state
        }
        with open(self.save_file, "w") as f:
            json.dump(data, f)

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