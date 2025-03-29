import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../src/data"))

class Inventory:
    def __init__(self):
        self.data_path = os.path.join(DATA_DIR, "inventory_data.json")
        self.items = self.load_inventory()

    def load_inventory(self):
        """Đọc dữ liệu từ inventory_data.json và kiểm tra cơ bản."""
        try:
            with open(self.data_path, "r") as f:
                loaded_data = json.load(f)
                required_keys = {
                    "carrot_seed", "cabbage_seed", "beetroot_seed", "pumpkin_seed",
                    "energy_herb_seed", "rare_herb_seed", "carrot", "cabbage", "tomato",
                    "potato", "beetroot", "pumpkin", "energy_herb", "rare_herb",
                    "tilapia", "carp", "catfish", "eel", "ghost_fish", "frog","basic_rod","gold_rod","diamond_rod"
                }
                for key in required_keys:
                    if key not in loaded_data:
                        raise KeyError(f"Thiếu trường bắt buộc: {key} trong {self.data_path}")
                    if isinstance(loaded_data[key], list):
                        loaded_data[key] = sum(loaded_data[key])  # Tính tổng nếu là danh sách số
                    elif not isinstance(loaded_data[key], int):
                        raise ValueError(f"Giá trị của {key} trong {self.data_path} phải là số nguyên hoặc danh sách số.")
                return loaded_data  # Giữ nguyên các trường khác như rods_owned
        except FileNotFoundError:
            raise FileNotFoundError(f"Lỗi: Không tìm thấy file {self.data_path}.")
        except json.JSONDecodeError:
            raise ValueError(f"Lỗi: File {self.data_path} không phải là định dạng JSON hợp lệ.")
        except KeyError as e:
            raise ValueError(f"Lỗi: {str(e)}.")

    def save_inventory(self, data=None):
        """Lưu dữ liệu vào inventory_data.json."""
        if data is None:
            data = self.items
        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=2)

    def add_item(self, item_name, quantity):
        """Thêm vật phẩm vào kho."""
        if not isinstance(quantity, int):
            raise ValueError("Số lượng phải là số nguyên.")
        if item_name in self.items:
            self.items[item_name] += quantity
            print(f"Đã thêm {quantity} {item_name} vào kho. Hiện có: {self.items[item_name]}")
        else:
            self.items[item_name] = quantity
            print(f"Đã thêm vật phẩm mới: {item_name} x{quantity}")
        self.save_inventory()

    def remove_item(self, item_name, quantity):
        """Xóa vật phẩm khỏi kho, trả về True nếu thành công."""
        if not isinstance(quantity, int):
            raise ValueError("Số lượng phải là số nguyên.")
        if item_name in self.items:
            if self.items[item_name] >= quantity:
                self.items[item_name] -= quantity
                print(f"Đã xóa {quantity} {item_name} khỏi kho. Còn lại: {self.items[item_name]}")
                self.save_inventory()
                return True
            else:
                print(f"Không đủ {item_name} trong kho để xóa! Hiện có: {self.items.get(item_name, 0)}")
                return False
        else:
            print(f"Vật phẩm {item_name} không tồn tại trong kho!")
            return False

    def get_item_quantity(self, item_name):
        """Trả về số lượng của một vật phẩm trong kho."""
        return self.items.get(item_name, 0) if isinstance(self.items.get(item_name), int) else 0

    def has_item(self, item_name, quantity=1):
        """Kiểm tra xem có đủ số lượng vật phẩm hay không."""
        return self.items.get(item_name, 0) >= quantity if isinstance(self.items.get(item_name), int) else False

    def get_all_items(self):
        """Trả về danh sách tất cả vật phẩm và số lượng."""
        return {item: qty for item, qty in self.items.items() if isinstance(qty, int) and qty > 0}

    def display_inventory(self):
        """Hiển thị toàn bộ kho đồ hiện tại, chỉ hiển thị các mục có số lượng là số nguyên."""
        print("=== Kho đồ ===")
        for item, quantity in self.items.items():
            if isinstance(quantity, int) and quantity > 0:  # Chỉ hiển thị nếu quantity là số nguyên
                print(f"{item}: {quantity}")
        print("=============")

if __name__ == "__main__":
    try:
        inventory = Inventory()
        inventory.display_inventory()  # Hiển thị kho ban đầu

        # Thử thêm vật phẩm
        inventory.add_item("tomato", 3)
        inventory.add_item("tilapia", 1)
        inventory.add_item("energy_herb", 1)

        # Thử xóa vật phẩm
        inventory.remove_item("carrot_seed", 1)
        inventory.remove_item("tomato", 2)

        # Kiểm tra số lượng
        print(f"Số lượng cà rốt: {inventory.get_item_quantity('carrot')}")
        print(f"Có đủ 2 hạt cà rốt không? {inventory.has_item('carrot_seed', 2)}")

        # Hiển thị kho cuối cùng
        inventory.display_inventory()
    except (FileNotFoundError, ValueError) as e:
        print(f"Lỗi: {e}")