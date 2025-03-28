import sys
import os
import json

save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
from src.core.inventory import Inventory

class Player:
    def __init__(self):
        self.energy = 100
        self.money = 100
        self.rod_level = "wood"
        self.max_energy = 100
        self.garden_slots = 4
        self.inventory = Inventory()

    def add_energy(self, amount):
        self.energy = min(self.max_energy, self.energy + amount)
        print(f"Năng lượng hiện tại: {self.energy}")

    def reduce_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            print(f"Năng lượng hiện tại: {self.energy}")
            return True
        else:
            print("Không đủ năng lượng!")
            return False

    def add_money(self, amount):
        self.money += amount
        print(f"Tiền hiện tại: {self.money} đồng")

    def spend_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            print(f"Tiền hiện tại: {self.money} đồng")
            return True
        else:
            print("Không đủ tiền!")
            return False

    def upgrade_rod(self, new_level):
        rod_costs = {"silver": 20, "gold": 25, "diamond": 32}
        current_levels = ["wood", "silver", "gold", "diamond"]
        if new_level not in rod_costs:
            print("Cấp cần câu không hợp lệ!")
            return False
        current_index = current_levels.index(self.rod_level)
        new_index = current_levels.index(new_level)
        if new_index <= current_index:
            print("Bạn đã có cần câu cấp này hoặc cao hơn!")
            return False
        if self.spend_money(rod_costs[new_level]):
            self.rod_level = new_level
            print(f"Đã nâng cấp cần câu lên {new_level}!")
            return True
        return False

    def upgrade_garden(self, new_slots):
        slot_costs = {6: 18, 8: 25, 10: 32}
        if new_slots not in slot_costs:
            print("Số ô không hợp lệ!")
            return False
        if new_slots <= self.garden_slots:
            print("Số ô mới phải lớn hơn số ô hiện tại!")
            return False
        if self.spend_money(slot_costs[new_slots]):
            self.garden_slots = new_slots
            print(f"Đã mở rộng vườn lên {new_slots} ô!")
            return True
        return False

    def get_energy(self):
        return self.energy

    def get_money(self):
        return self.money

    def get_rod_level(self):
        return self.rod_level

    def get_garden_slots(self):
        return self.garden_slots

    def to_dict(self):
        return {
            "energy": self.energy,
            "money": self.money,
            "rod_level": self.rod_level,
            "max_energy": self.max_energy,
            "garden_slots": self.garden_slots,
            "inventory": self.inventory.items
        }

    def load_from_dict(self, data):
        self.energy = data.get("energy", 100)
        self.money = data.get("money", 100)
        self.rod_level = data.get("rod_level", "wood")
        self.max_energy = data.get("max_energy", 100)
        self.garden_slots = data.get("garden_slots", 4)
        self.inventory.items = data.get("inventory", {})

if __name__ == "__main__":
    player = Player()
    print(f"Năng lượng ban đầu: {player.get_energy()}")
    print(f"Tiền ban đầu: {player.get_money()}")
    player.inventory.display_inventory()