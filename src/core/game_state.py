import os
import json
from src.core.player import Player
from src.core.time_system import TimeSystem

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")  # Thư mục lưu trữ mới

class GameState:
    def __init__(self):
        self.player = Player()
        self.time_system = TimeSystem()
        self.FARM_DATA_FILE = os.path.join(DATA_DIR, "farm_data.json")  # Cập nhật đường dẫn
        self.PLAYER_DATA_FILE = os.path.join(DATA_DIR, "player_data.json")  # Cập nhật đường dẫn
        self.TIME_DATA_FILE = os.path.join(DATA_DIR, "time_data.json")  # Cập nhật đường dẫn
        self.planted_seeds = self.load_farm_data()
        self.load_player_data()
        self.time_system.load_time_data()
        self.time_system.load_plants(self.planted_seeds)

    def load_farm_data(self):
        try:
            with open(self.FARM_DATA_FILE, "r") as f:
                farm_data = json.load(f)
                return {int(index): {
                    "seed": plant["seed"],
                    "stage": plant["stage"],
                    "remaining_upgrade_time": plant["remaining_upgrade_time"],
                    "remaining_death_time": plant["remaining_death_time"],
                    "center_pos": tuple(plant["center_pos"])
                } for index, plant in farm_data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_player_data(self):
        try:
            with open(self.PLAYER_DATA_FILE, "r") as f:
                player_data = json.load(f)
                self.player.load_from_dict(player_data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_game(self):
        # Đảm bảo thư mục src/data tồn tại
        os.makedirs(DATA_DIR, exist_ok=True)

        # Lưu dữ liệu thời gian
        self.time_system.save_time_data()  # Giả sử save_time_data đã được cập nhật để dùng TIME_DATA_FILE
        
        # Lưu dữ liệu nông trại
        farm_data = {str(index): {
            "seed": plant["seed"],
            "stage": plant["stage"],
            "remaining_upgrade_time": plant["remaining_upgrade_time"],
            "remaining_death_time": plant["remaining_death_time"],
            "center_pos": plant["center_pos"]
        } for index, plant in self.planted_seeds.items()}
        with open(self.FARM_DATA_FILE, "w") as f:
            json.dump(farm_data, f)
        
        # Lưu dữ liệu người chơi
        player_data = self.player.to_dict()
        with open(self.PLAYER_DATA_FILE, "w") as f:
            json.dump(player_data, f)