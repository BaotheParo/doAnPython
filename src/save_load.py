import os
import json
from src.core.player import Player
from src.core.inventory import Inventory

SAVE_DIR = "saves"

class SaveLoad:
    @staticmethod
    def save_game(player):
        """Lưu trạng thái game. Nếu save1.dat đã tồn tại, tự động tạo save2.dat, save3.dat,..."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        existing_saves = [f for f in os.listdir(SAVE_DIR) if f.startswith("save") and f.endswith(".dat")]
        save_numbers = []
        for filename in existing_saves:
            try:
                num = int(filename[4:-4])  # cắt 'save' và '.dat'
                save_numbers.append(num)
            except ValueError:
                pass

        if save_numbers:
            next_save_number = max(save_numbers) + 1
        else:
            next_save_number = 1

        save_filename = f"save{next_save_number}.dat"
        save_path = os.path.join(SAVE_DIR, save_filename)

        save_data = {
            "energy": player.energy,
            "money": player.money,
            "inventory": player.inventory.items
        }

        with open(save_path, "w") as file:
            json.dump(save_data, file)

        print(f"Game saved to {save_filename}!")

    @staticmethod
    def load_game(filename="save1.dat"):
        """Load game từ save1.dat hoặc chỉ định file khác."""
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
        """Trả về danh sách file save (*.dat)."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        return [f for f in os.listdir(SAVE_DIR) if f.endswith(".dat")]

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
        """Kiểm tra save1.dat có trống không."""
        save_path = os.path.join(SAVE_DIR, "save1.dat")
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
        """Reset save1.dat về mặc định trống."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        empty_data = {
            "energy": 0,
            "money": 0,
            "inventory": []
        }

        save_path = os.path.join(SAVE_DIR, "save1.dat")
        with open(save_path, "w") as file:
            json.dump(empty_data, file)

        print("Save1.dat reset to empty.")

    @staticmethod
    def backup_save():
        """Sao lưu save1.dat thành save2.dat, save3.dat..."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        src = os.path.join(SAVE_DIR, "save1.dat")
        if not os.path.exists(src):
            print("No save1.dat to backup.")
            return

        existing_saves = [f for f in os.listdir(SAVE_DIR) if f.startswith("save") and f.endswith(".dat")]
        save_numbers = []
        for filename in existing_saves:
            try:
                num = int(filename[4:-4])
                save_numbers.append(num)
            except ValueError:
                pass

        if save_numbers:
            next_number = max(save_numbers) + 1
        else:
            next_number = 2  # Backup thì bắt đầu từ save2.dat

        dst = os.path.join(SAVE_DIR, f"save{next_number}.dat")
        with open(src, "rb") as f_src, open(dst, "wb") as f_dst:
            f_dst.write(f_src.read())

        print(f"Backed up save1.dat to save{next_number}.dat")
