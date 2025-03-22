import json
import os


class Inventory:
    def __init__(self):
        # Đường dẫn tương đối đến file inventory_data.json
        self.data_path = "../data/inventory_data.json"

        # Khởi tạo kho đồ từ file JSON
        self.items = self.load_inventory()

    def load_inventory(self):
        """Đọc dữ liệu từ inventory_data.json."""
        try:
            with open(self.data_path, "r") as f:
                loaded_data = json.load(f)
                # Đảm bảo tất cả các trường cần thiết có trong dữ liệu
                required_keys = {
                    "carrot_seed", "cabbage_seed", "beetroot_seed", "pumpkin_seed",
                    "energy_herb_seed", "rare_herb_seed", "carrot", "cabbage", "tomato",
                    "potato", "beetroot", "pumpkin", "energy_herb", "rare_herb",
                    "tilapia", "carp", "catfish", "eel", "ghost_fish", "frog",
                    "rods_owned", "current_rod"
                }
                for key in required_keys:
                    if key not in loaded_data:
                        raise KeyError(f"Thiếu trường bắt buộc: {key} trong {self.data_path}")
                return loaded_data
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Lỗi: Không tìm thấy file {self.data_path}. Vui lòng tạo file inventory_data.json trong thư mục data/ với dữ liệu hợp lệ.")
        except json.JSONDecodeError:
            raise ValueError(f"Lỗi: File {self.data_path} không phải là định dạng JSON hợp lệ.")
        except KeyError as e:
            raise ValueError(f"Lỗi: {str(e)}. Vui lòng kiểm tra lại cấu trúc file {self.data_path}.")

    def save_inventory(self, data=None):
        """Lưu dữ liệu vào inventory_data.json."""
        if data is None:
            data = self.items
        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=2)

    def add_item(self, item_name, quantity):
        """Thêm vật phẩm vào kho."""
        if item_name in self.items and item_name not in ["rods_owned", "current_rod"]:
            self.items[item_name] += quantity
            print(f"Đã thêm {quantity} {item_name} vào kho. Hiện có: {self.items[item_name]}")
        else:
            if item_name not in ["rods_owned", "current_rod"]:
                self.items[item_name] = quantity
                print(f"Đã thêm vật phẩm mới: {item_name} x{quantity}")
        self.save_inventory()  # Lưu sau khi thay đổi

    def add_rod(self, rod_name):
        """Thêm một cần câu vào danh sách rods_owned và đặt làm cần câu hiện tại."""
        if rod_name not in self.items["rods_owned"]:
            self.items["rods_owned"].append(rod_name)
            self.items["current_rod"] = rod_name  # Đặt cần câu mới mua làm cần câu hiện tại
            print(f"Đã mua cần câu {rod_name}. Cần câu hiện tại: {self.items['current_rod']}")
            self.save_inventory()  # Lưu sau khi thay đổi
        else:
            print(f"Bạn đã sở hữu cần câu {rod_name} rồi!")

    def remove_item(self, item_name, quantity):
        """Xóa vật phẩm khỏi kho, trả về True nếu thành công."""
        if item_name in self.items and item_name not in ["rods_owned", "current_rod"]:
            if self.items[item_name] >= quantity:
                self.items[item_name] -= quantity
                print(f"Đã xóa {quantity} {item_name} khỏi kho. Còn lại: {self.items[item_name]}")
                self.save_inventory()  # Lưu sau khi thay đổi
                return True
            else:
                print(f"Không đủ {item_name} trong kho để xóa! Hiện có: {self.items.get(item_name, 0)}")
                return False
        else:
            print(f"Vật phẩm {item_name} không tồn tại trong kho!")
            return False

    def get_item_quantity(self, item_name):
        """Trả về số lượng của một vật phẩm trong kho."""
        if item_name in ["rods_owned", "current_rod"]:
            return self.items.get(item_name, [])
        return self.items.get(item_name, 0)

    def has_item(self, item_name, quantity=1):
        """Kiểm tra xem có đủ số lượng vật phẩm hay không."""
        if item_name in ["rods_owned", "current_rod"]:
            return item_name in self.items
        return self.items.get(item_name, 0) >= quantity

    def get_all_items(self):
        """Trả về danh sách tất cả vật phẩm và số lượng."""
        return {item: qty for item, qty in self.items.items() if item not in ["rods_owned", "current_rod"] and qty > 0}

    def display_inventory(self):
        """Hiển thị toàn bộ kho đồ hiện tại."""
        print("=== Kho đồ ===")
        for item, quantity in self.items.items():
            if item not in ["rods_owned", "current_rod"] and quantity > 0:
                print(f"{item}: {quantity}")
        print(f"Cần câu sở hữu: {self.items.get('rods_owned', [])}")
        print(f"Cần câu hiện tại: {self.items.get('current_rod', 'basic_rod')}")
        print("=============")


# Ví dụ chạy thử
if __name__ == "__main__":
    try:
        inventory = Inventory()
        inventory.display_inventory()  # Hiển thị kho ban đầu

        # Thử thêm vật phẩm
        inventory.add_item("tomato", 3)  # Thu hoạch 3 cà chua
        inventory.add_item("tilapia", 1)  # Câu được 1 cá rô phi
        inventory.add_item("energy_herb", 1)  # Thu hoạch thảo mộc tăng năng lượng

        # Thử xóa vật phẩm
        inventory.remove_item("carrot_seed", 1)  # Dùng 1 hạt cà rốt để trồng
        inventory.remove_item("tomato", 2)  # Bán 2 cà chua

        # Kiểm tra số lượng
        print(f"Số lượng cà rốt: {inventory.get_item_quantity('carrot')}")
        print(f"Có đủ 2 hạt cà rốt không? {inventory.has_item('carrot_seed', 2)}")

        # Hiển thị kho cuối cùng
        inventory.display_inventory()
    except (FileNotFoundError, ValueError) as e:
        print(f"Lỗi: {e}")