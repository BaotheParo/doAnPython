class Inventory:
    def __init__(self):
        # Khởi tạo kho đồ rỗng dưới dạng từ điển: {tên vật phẩm: số lượng}
        self.items = {
            # Hạt giống
            "carrot_seed": 2,
            "cabbage_seed": 0,
            "beetroot_seed ": 0,
            "pumpkin_seed": 0,
            "energy_herb_seed": 0,
            "rare_herb_seed": 0,
            # Nông sản
            "carrot": 0,
            "cabbage": 0,
            "tomato": 0,
            "potato": 0,
            "energy_herb": 0,
            "rare_herb": 0,
            # Ngư sản
            "tilapia": 0,
            "carp": 0,
            "catfish": 0,
            "eel": 0,
            "ghost_fish": 0,
            "frog": 0
        }

    def add_item(self, item_name, quantity):
        """Thêm vật phẩm vào kho."""
        if item_name in self.items:
            self.items[item_name] += quantity
            print(f"Đã thêm {quantity} {item_name} vào kho. Hiện có: {self.items[item_name]}")
        else:
            self.items[item_name] = quantity
            print(f"Đã thêm vật phẩm mới: {item_name} x{quantity}")

    def remove_item(self, item_name, quantity):
        """Xóa vật phẩm khỏi kho, trả về True nếu thành công."""
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            print(f"Đã xóa {quantity} {item_name} khỏi kho. Còn lại: {self.items[item_name]}")
            return True
        else:
            print(f"Không đủ {item_name} trong kho để xóa! Hiện có: {self.items.get(item_name, 0)}")
            return False

    def get_item_quantity(self, item_name):
        """Trả về số lượng của một vật phẩm trong kho."""
        return self.items.get(item_name, 0)

    def has_item(self, item_name, quantity=1):
        """Kiểm tra xem có đủ số lượng vật phẩm hay không."""
        return self.items.get(item_name, 0) >= quantity

    def get_all_items(self):
        """Trả về danh sách tất cả vật phẩm và số lượng."""
        return {item: qty for item, qty in self.items.items() if qty > 0}

    def display_inventory(self):
        """Hiển thị toàn bộ kho đồ hiện tại."""
        print("=== Kho đồ ===")
        for item, quantity in self.items.items():
            if quantity > 0:
                print(f"{item}: {quantity}")
        print("=============")

# Ví dụ chạy thử
if __name__ == "__main__":
    inventory = Inventory()
    inventory.display_inventory()  # Hiển thị kho ban đầu

    # Thử thêm vật phẩm
    inventory.add_item("tomato", 3)       # Thu hoạch 3 cà chua
    inventory.add_item("tilapia", 1)      # Câu được 1 cá rô phi
    inventory.add_item("energy_herb", 1)  # Thu hoạch thảo mộc tăng năng lượng

    # Thử xóa vật phẩm
    inventory.remove_item("carrot_seed", 1)  # Dùng 1 hạt cà rốt để trồng
    inventory.remove_item("tomato", 2)       # Bán 2 cà chua

    # Kiểm tra số lượng
    print(f"Số lượng cà rốt: {inventory.get_item_quantity('carrot')}")
    print(f"Có đủ 2 hạt cà rốt không? {inventory.has_item('carrot_seed', 2)}")

    # Hiển thị kho cuối cùng
    inventory.display_inventory()