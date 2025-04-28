import os
import json
from src.core.player import Player
from src.core.inventory import Inventory

SAVE_DIR = "saves"

class SaveLoad:
    current_save_file = None  # Theo dõi file save hiện tại

    @staticmethod
    def ensure_save_folder():
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

    @staticmethod
    def save_game(player, filename=None):
        """Lưu trạng thái game vào file cụ thể. Nếu không có filename thì lưu vào current_save_file."""
        SaveLoad.ensure_save_folder()

        if filename:
            filename = os.path.basename(filename)  
            SaveLoad.current_save_file = filename
        elif SaveLoad.current_save_file is None:
            SaveLoad.current_save_file = SaveLoad.get_new_save_filename()

        save_path = os.path.join(SAVE_DIR, SaveLoad.current_save_file)

        save_data = {
            "energy": player.energy,
            "money": player.money,
            "inventory": player.inventory.items
        }

        with open(save_path, "w") as file:
            json.dump(save_data, file, indent=4)

        print(f"Game saved to {SaveLoad.current_save_file}!")


    @staticmethod
    def load_game(filename=None):
        """Load trạng thái game từ file cụ thể, nếu không thì từ current_save_file."""
        SaveLoad.ensure_save_folder()

        if filename:
            SaveLoad.current_save_file = os.path.basename(filename)

        if SaveLoad.current_save_file is None:
            print("No save file specified.")
            return Player()

        save_path = os.path.join(SAVE_DIR, SaveLoad.current_save_file)

        if not os.path.exists(save_path):
            print(f"No save file '{SaveLoad.current_save_file}' found. Creating new player.")
            return Player()

        with open(save_path, "r") as file:
            save_data = json.load(file)

        player = Player()
        player.energy = save_data.get("energy", 0)
        player.money = save_data.get("money", 0)
        player.inventory = Inventory()
        player.inventory.items = save_data.get("inventory", [])

        print(f"Game loaded from {SaveLoad.current_save_file}!")
        return player

    @staticmethod
    def list_save_files():
        """Trả về danh sách file save (*.json)."""
        SaveLoad.ensure_save_folder()
        return sorted([f for f in os.listdir(SAVE_DIR) if f.endswith(".json")])

    @staticmethod
    def load_selected_save(filepath):
        """Load player từ filepath (đầy đủ đường dẫn)."""
        if not os.path.isfile(filepath):
            print(f"File {filepath} not found.")
            return None

        with open(filepath, "r") as file:
            save_data = json.load(file)

        player = Player()
        player.energy = save_data.get("energy", 0)
        player.money = save_data.get("money", 0)
        player.inventory = Inventory()
        player.inventory.items = save_data.get("inventory", [])

        SaveLoad.current_save_file = os.path.basename(filepath)
        print(f"Game loaded from {filepath}!")
        return player

    @staticmethod
    def get_new_save_filename():
        """Tìm filename mới dạng save_slot_x.json."""
        SaveLoad.ensure_save_folder()

        existing_files = SaveLoad.list_save_files()
        numbers = []

        for filename in existing_files:
            try:
                num = int(filename.replace("save_slot_", "").replace(".json", ""))
                numbers.append(num)
            except ValueError:
                pass

        next_num = max(numbers, default=0) + 1
        return f"save_slot_{next_num}.json"

    @staticmethod
    def is_empty_save():
        """Kiểm tra thư mục save có file nào không."""
        SaveLoad.ensure_save_folder()
        return len(SaveLoad.list_save_files()) == 0

    @staticmethod
    def reset_save(filename=None):
        """Reset file save chỉ định hoặc file hiện tại."""
        SaveLoad.ensure_save_folder()

        if filename:
            target_file = os.path.basename(filename)
        elif SaveLoad.current_save_file:
            target_file = SaveLoad.current_save_file
        else:
            print("No file specified to reset.")
            return

        empty_data = {
            "energy": 0,
            "money": 0,
            "inventory": []
        }

        save_path = os.path.join(SAVE_DIR, target_file)
        with open(save_path, "w") as file:
            json.dump(empty_data, file, indent=4)

        print(f"{target_file} reset to empty.")

    @staticmethod
    def backup_save(source_filename=None):
        """Backup file save thành bản copy mới."""
        SaveLoad.ensure_save_folder()

        if source_filename:
            src = os.path.join(SAVE_DIR, os.path.basename(source_filename))
        elif SaveLoad.current_save_file:
            src = os.path.join(SAVE_DIR, SaveLoad.current_save_file)
        else:
            print("No file specified to backup.")
            return

        if not os.path.isfile(src):
            print(f"No file {src} to backup.")
            return

        backup_filename = SaveLoad.get_new_save_filename()
        dst = os.path.join(SAVE_DIR, backup_filename)

        with open(src, "r") as f_src, open(dst, "w") as f_dst:
            data = json.load(f_src)
            json.dump(data, f_dst, indent=4)

        print(f"Backup {os.path.basename(src)} to {backup_filename}")

