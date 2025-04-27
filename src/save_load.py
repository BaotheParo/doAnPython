import os  # Đảm bảo import thư viện os
import json
from src.core.player import Player
from src.core.inventory import Inventory  # Thêm nếu Inventory cần được nhập

SAVE_DIR = "saves"  # Đảm bảo thư mục saves tồn tại

class SaveLoad:
    @staticmethod
    def save_game(player):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        
        save_data = {
            "energy": player.energy,
            "money": player.money,
            "inventory": player.inventory.items
        }
        
        # Lưu dữ liệu vào file save1.dat
        with open(os.path.join(SAVE_DIR, "save1.dat"), "w") as file:
            json.dump(save_data, file)
    
    @staticmethod
    def load_game():
        try:
            with open(os.path.join(SAVE_DIR, "save1.dat"), "r") as file:
                save_data = json.load(file)
                player = Player()
                player.energy = save_data["energy"]
                player.money = save_data["money"]
                player.inventory = Inventory()
                player.inventory.items = save_data["inventory"]
                return player
        except FileNotFoundError:
            print("No save file found, creating a new player.")
            return Player()

    @staticmethod
    def load_select():
        # Danh sách các file lưu trong thư mục saves
        save_files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".dat")]
        
        if save_files:
            print("Available saved games:")
            for idx, file in enumerate(save_files, start=1):
                print(f"{idx}: {file}")
            
            # Giả lập việc chọn file (ở đây chọn file đầu tiên)
            selected_file = save_files[0]  # Bạn có thể thêm lựa chọn người dùng ở đây
            save_path = os.path.join(SAVE_DIR, selected_file)

            with open(save_path, "r") as file:
                save_data = json.load(file)
                player = Player()
                player.energy = save_data["energy"]
                player.money = save_data["money"]
                player.inventory = Inventory()
                player.inventory.items = save_data["inventory"]
                print(f"Game loaded from {selected_file}!")
                return player
        else:
            print("No saved games found.")
            return None
