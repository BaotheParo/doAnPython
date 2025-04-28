import os
import json
from src.core.player import Player
from src.core.inventory import Inventory

SAVE_DIR = "saves"

class SaveLoad:
    @staticmethod
    def save_game(player):
        """Lưu trạng thái game. Nếu save_data_1.json đã tồn tại, tự động tạo save_data_2.json, save_data_3.json,..."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        existing_saves = [f for f in os.listdir(SAVE_DIR) if f.startswith("save_data_") and f.endswith(".json")]
        save_numbers = []
        for filename in existing_saves:
            try:
                num = int(filename[len("save_data_"):-len(".json")])
                save_numbers.append(num)
            except ValueError:
                pass

        if save_numbers:
            next_save_number = max(save_numbers) + 1
        else:
            next_save_number = 1

        save_filename = f"save_data_{next_save_number}.json"
        save_path = os.path.join(SAVE_DIR, save_filename)

        save_data = {
            "energy": player.energy,
            "money": player.money,
            "inventory": player.inventory.items
        }

        with open(save_path, "w") as file:
            json.dump(save_data, file, indent=4)

        print(f"Game saved to {save_filename}!")

    @staticmethod
    def load_game(filename="save_data_1.json"):
        """Load game từ save_data_1.json hoặc file chỉ định khác."""
        save_path = os.path.join(SAVE_DIR, filename)
        if not os.path.exists(save_path):
            print(f"No save file '{filename}' found, creating a new player.")
            return Player()

        with open(save_path, "r") as file:
            save_data = json.load(file)
            player = Player()
            player.energy = save_data.get("energy", 0)
            player.money = save_data.get("money", 0)
            player.inventory = Inventory()
            player.inventory.items = save_data.get("inventory", [])
            print(f"Game loaded from {filename}!")
            return player

    @staticmethod
    def list_save_files():
        """Trả về danh sách file save (*.json)."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        return [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]

    @staticmethod
    def load_selected_save(selected_filename):
        """Load từ file save cụ thể."""
        save_path = os.path.join(SAVE_DIR, selected_filename)
        if not os.path.exists(save_path):
            print(f"File {selected_filename} not found.")
            return None

        with open(save_path, "r") as file:
            save_data = json.load(file)
            player = Player()
            player.energy = save_data.get("energy", 0)
            player.money = save_data.get("money", 0)
            player.inventory = Inventory()
            player.inventory.items = save_data.get("inventory", [])
            print(f"Game loaded from {selected_filename}!")
            return player

    @staticmethod
    def is_empty_save():
        """Kiểm tra save_data_1.json có trống không."""
        save_path = os.path.join(SAVE_DIR, "save_data_1.json")
        if not os.path.exists(save_path):
            return True
        try:
            with open(save_path, "r") as file:
                save_data = json.load(file)
                return all(value == 0 or value == [] for value in save_data.values())
        except (json.JSONDecodeError, IOError):
            return True

    @staticmethod
    def reset_save():
        """Reset save_data_1.json về mặc định trống."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        empty_data = {
            "energy": 0,
            "money": 0,
            "inventory": []
        }

        save_path = os.path.join(SAVE_DIR, "save_data_1.json")
        with open(save_path, "w") as file:
            json.dump(empty_data, file, indent=4)

        print("save_data_1.json reset to empty.")

    @staticmethod
    def backup_save():
        """Sao lưu save_data_1.json thành save_data_2.json, save_data_3.json..."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        src = os.path.join(SAVE_DIR, "save_data_1.json")
        if not os.path.exists(src):
            print("No save_data_1.json to backup.")
            return

        existing_saves = [f for f in os.listdir(SAVE_DIR) if f.startswith("save_data_") and f.endswith(".json")]
        save_numbers = []
        for filename in existing_saves:
            try:
                num = int(filename[len("save_data_"):-len(".json")])
                save_numbers.append(num)
            except ValueError:
                pass

        if save_numbers:
            next_number = max(save_numbers) + 1
        else:
            next_number = 2  # Backup thì bắt đầu từ save_data_2.json

        dst = os.path.join(SAVE_DIR, f"save_data_{next_number}.json")
        with open(src, "r") as f_src, open(dst, "w") as f_dst:
            data = json.load(f_src)
            json.dump(data, f_dst, indent=4)

        print(f"Backed up save_data_1.json to save_data_{next_number}.json")
