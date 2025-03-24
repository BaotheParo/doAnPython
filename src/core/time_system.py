import pygame
import json
import os

class TimeSystem:
    def __init__(self, filename="time_data.json"):
        save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.save_file = os.path.join(save_dir, filename)
        
        self.day_duration = 50000  # Ban ngày = 50,000 ms
        self.night_duration = 10000  # Ban đêm = 10,000 ms
        self.day_length = self.day_duration + self.night_duration  # Tổng thời gian của ngày (60,000 ms)
        self.UPGRADE_TIME = 60000  # 60 giây để cây phát triển mỗi giai đoạn
        self.DEATH_TIME = 120000  # 120 giây để cây chết nếu không được tưới
        self.planted_seeds = {}  # Quản lý cây trồng trong TimeSystem
        self.load_time_data()

    def load_time_data(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.current_day = data.get("current_day", 0)
                self.remaining_day_time = data.get("remaining_day_time", self.day_duration)
                self.is_day_state = data.get("is_day_state", True)
                self.last_update_time = data.get("last_update_time", pygame.time.get_ticks())
                elapsed_time = pygame.time.get_ticks() - self.last_update_time
                if elapsed_time > 0 and self.planted_seeds:
                    self.update_plants(elapsed_time)
        else:
            self.current_day = 0
            self.remaining_day_time = self.day_duration
            self.is_day_state = True
            self.last_update_time = pygame.time.get_ticks()

    def save_time_data(self):
        # Chỉ lưu khi được gọi từ UI, không tự động lưu
        data = {
            "current_day": self.current_day,
            "remaining_day_time": self.remaining_day_time,
            "is_day_state": self.is_day_state,
            "last_update_time": pygame.time.get_ticks()
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
        self.update_plants(delta_time)

    def update_plants(self, delta_time):
        for index in list(self.planted_seeds.keys()):
            plant = self.planted_seeds[index]
            if plant["stage"] >= 3:  # Đã trưởng thành hoặc chết
                continue
            plant["remaining_death_time"] -= delta_time
            if plant["remaining_death_time"] <= 0 and plant["stage"] < 4:
                plant["stage"] = 4  # Cây chết
                plant["remaining_upgrade_time"] = None
                print(f"Plant at plot {index} has died!")
            if plant["remaining_upgrade_time"] is not None:
                plant["remaining_upgrade_time"] -= delta_time
                if plant["remaining_upgrade_time"] <= 0:
                    plant["stage"] += 1
                    if plant["stage"] < 3:
                        plant["remaining_upgrade_time"] = None
                        plant["remaining_death_time"] = self.DEATH_TIME
                    else:
                        plant["remaining_upgrade_time"] = None
                        plant["remaining_death_time"] = None
                    print(f"Plant at plot {index} upgraded to stage {plant['stage']}!")
                    if plant["stage"] == 3:
                        print(f"Plant at plot {index} is fully grown!")

    def load_plants(self, planted_seeds):
        self.planted_seeds = planted_seeds

    def get_plants(self):
        return self.planted_seeds

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