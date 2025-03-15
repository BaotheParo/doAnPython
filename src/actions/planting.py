import pygame
import sys
import json
sys.path.append("D:\\ĐHSG\\Python\\Project\\doAnPython\\src\\core")
from inventory import Inventory
from player import Player

# Khởi tạo pygame
pygame.init()

# Cấu hình màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nông trại")

# Load hình ảnh nền
farm_bg = pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\backgrounds\\khuvuon.png")
farm_bg = pygame.transform.scale(farm_bg, (WIDTH, HEIGHT))

plant_images = {
    "carrot_seed": {
        0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\carot.png"), (40, 40)),
        1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\seed.png"), (50, 50)),
        2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\carot1.png"), (40, 40)),
        3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\carot2.png"), (70, 70)),
    },
    "cabbage_seed": {
        0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\bapcai.png"), (40, 40)),
        1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\seed.png"), (50, 50)),
        2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\bapcai1.png"), (40, 40)),
        3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\bapcai2.png"), (70, 70)),
    },
    "beetroot_seed": {
        0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\cuden.png"), (40, 40)),
        1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\seed.png"), (50, 50)),
        2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\cuden1.png"), (40, 40)),
        3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\cuden2.png"), (70, 70)),
    },
    "pumpkin_seed": {
        0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\bido.png"), (40, 40)),
        1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\seed.png"), (50, 50)),
        2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\bido1.png"), (40, 40)),
        3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\bido2.png"), (70, 70)),
    },
    "energy_herb_seed": {
        0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\thaomoc.png"), (40, 40)),
        1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\seed.png"), (50, 50)),
        2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\thaomoc1.png"), (40, 40)),
        3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\thaomoc2.png"), (70, 70)),
    },
    "rare_herb_seed": {
        0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\lua.png"), (40, 40)),
        1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\seed.png"), (50, 50)),
        2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\lua1.png"), (40, 40)),
        3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\lua2.png"), (70, 70)),
    },
}

seed_names = {
    "carrot_seed": "Carrot Seed",
    "cabbage_seed": "Cabbage Seed",
    "beetroot_seed": "Beetroot Seed",
    "pumpkin_seed": "Pumpkin Seed",
    "energy_herb_seed": "Energy Herb Seed",
    "rare_herb_seed": "Rare Herb Seed",
}

# Màu sắc phong cách pixel
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INVENTORY_BG = (100, 70, 50)
INVENTORY_CELL_BG = (70, 50, 40)
BUTTON_COLOR = (150, 150, 150)

# Định nghĩa các ô đất
plots = [
    pygame.Rect(176, 330, 120, 50),
    pygame.Rect(326, 330, 80, 50),
    pygame.Rect(446, 330, 100, 50),
    pygame.Rect(583, 332, 120, 50),
    pygame.Rect(156, 409, 120, 50),
    pygame.Rect(312, 412, 85, 50),
    pygame.Rect(437, 409, 100, 50),
    pygame.Rect(588, 414, 90, 50)
]

# Định nghĩa các nút feature
features = [
    {"rect": pygame.Rect(318, 35, 58, 78), "function": "plant_menu", "label": "Planting"},
    {"rect": pygame.Rect(386, 35, 58, 78), "function": "water", "label": "Watering"},
    {"rect": pygame.Rect(450, 35, 58, 78), "function": "remove", "label": "Remove"},
    {"rect": pygame.Rect(518, 35, 58, 78), "function": "harvest", "label": "Harvest"},
]

# Ánh xạ hạt giống với sản phẩm thu hoạch
seed_to_product = {
    "carrot_seed": "carrot",
    "cabbage_seed": "cabbage",
    "beetroot_seed": "beetroot",
    "pumpkin_seed": "pumpkin",
    "energy_herb_seed": "energy_herb",
    "rare_herb_seed": "rare_herb",
}

# Khởi tạo người chơi
player = Player()
ENERGY_COST = 20

# Biến lưu trạng thái
planted_seeds = {}
font = pygame.font.Font(None, 24)
default_cursor = pygame.SYSTEM_CURSOR_ARROW
hover_cursor = pygame.SYSTEM_CURSOR_HAND
sickle_cursor = pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\ll.png")
sickle_cursor = pygame.transform.scale(sickle_cursor, (32, 32))
watering_can_cursor = pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\watering_can.png")
watering_can_cursor = pygame.transform.scale(watering_can_cursor, (32, 32))
show_inventory = False
selected_seed = None
is_harvesting = False
is_watering = False
current_page = 0

# Thời gian mỗi giai đoạn và chu kỳ tưới nước (ms)
STAGE_DURATION = 5000
WATERING_CYCLE = 24000

# Hàm lưu inventory vào file
def save_inventory():
    with open("D:\\ĐHSG\\Python\\Project\\doAnPython\\src\\core\\inventory_data.json", "w") as f:
        json.dump(player.inventory.items, f)
    print("Đã lưu inventory vào file")

# Hàm tải inventory từ file
def load_inventory():
    try:
        with open("D:\\ĐHSG\\Python\\Project\\doAnPython\\src\\core\\inventory_data.json", "r") as f:
            player.inventory.items = json.load(f)
        print("Đã tải inventory từ file")
    except FileNotFoundError:
        print("Không tìm thấy file inventory, sử dụng mặc định")

# Tải inventory khi bắt đầu
load_inventory()

# Cấu hình inventory giao diện
inventory_rows = 2
inventory_cols = 5
inventory_cell_size = 50
inventory_padding = 10
inventory_width = inventory_cols * inventory_cell_size + inventory_padding * 2
inventory_height = inventory_rows * inventory_cell_size + inventory_padding * 2 + 40
inventory_x = WIDTH // 2 - inventory_width // 2
inventory_y = HEIGHT // 2 - inventory_height // 2
total_slots = inventory_rows * inventory_cols

# Nút phân trang
prev_button = pygame.Rect(inventory_x + inventory_padding, inventory_y + inventory_height - 30, 50, 20)
next_button = pygame.Rect(inventory_x + inventory_width - inventory_padding - 50, inventory_y + inventory_height - 30, 50, 20)

# Hàm cập nhật inventory giao diện với phân trang
def update_inventory_display():
    global current_page
    inventory_items = []
    seed_items = {k: v for k, v in player.inventory.get_all_items().items() if k.endswith("_seed")}
    for item_name, quantity in seed_items.items():
        for _ in range(quantity):
            inventory_items.append({"name": item_name, "image": plant_images[item_name][0]})
    
    total_items = len(inventory_items)
    total_pages = (total_items + total_slots - 1) // total_slots
    current_page = max(0, min(current_page, total_pages - 1)) if total_pages > 0 else 0
    
    start_index = current_page * total_slots
    end_index = min(start_index + total_slots, total_items)
    visible_items = inventory_items[start_index:end_index]
    
    while len(visible_items) < total_slots:
        visible_items.append({"name": None, "image": None})
    
    for i, item in enumerate(visible_items):
        row = i // inventory_cols
        col = i % inventory_cols
        item["rect"] = pygame.Rect(
            inventory_x + inventory_padding + col * inventory_cell_size,
            inventory_y + inventory_padding + row * inventory_cell_size,
            inventory_cell_size,
            inventory_cell_size
        )
    
    return visible_items, total_pages

# Hàm cập nhật giai đoạn cây trồng và kiểm tra tưới nước
def update_plant_stages():
    current_time = pygame.time.get_ticks()
    for index in list(planted_seeds.keys()):
        plant = planted_seeds[index]
        time_elapsed = current_time - plant["time_planted"]
        new_stage = min(3, 1 + (time_elapsed // STAGE_DURATION))
        planted_seeds[index]["stage"] = new_stage
        
        # Kiểm tra tưới nước
        time_since_last_watered = current_time - plant.get("last_watered", plant["time_planted"])
        if time_since_last_watered > WATERING_CYCLE:
            print(f"Cây tại ô {index} đã chết do không được tưới nước!")
            del planted_seeds[index]

running = True
while running:
    screen.blit(farm_bg, (0, 0))

    # Cập nhật giai đoạn cây trồng và kiểm tra tưới nước
    update_plant_stages()

    # Vẽ ô đất
    for index, plot in enumerate(plots):
        pygame.draw.rect(screen, BROWN, plot, 3)
        if index in planted_seeds:
            seed_type = planted_seeds[index]["seed"]
            stage = planted_seeds[index]["stage"]
            center_pos = planted_seeds[index]["center_pos"]  # Tâm điểm ô đất
            image = plant_images[seed_type][stage]
            # Tính toán vị trí để tâm hình ảnh trùng với tâm ô đất
            img_x = center_pos[0] - image.get_width() // 2
            img_y = center_pos[1] - image.get_height() // 2
            screen.blit(image, (img_x, img_y))

    # Lấy vị trí chuột
    mouse_pos = pygame.mouse.get_pos()

    # Vẽ các nút feature
    for feature in features:
        pygame.draw.rect(screen, BLUE, feature["rect"], 3)

    # Vẽ thanh năng lượng
    pygame.draw.rect(screen, WHITE, (20, 20, 104, 24))
    pygame.draw.rect(screen, BLUE, (22, 22, player.get_energy(), 20))
    energy_text = font.render(f"Năng lượng: {player.get_energy()}/{player.max_energy}", True, WHITE)
    screen.blit(energy_text, (20, 50))

    # Vẽ inventory nếu được kích hoạt
    if show_inventory:
        inventory_items, total_pages = update_inventory_display()
        pygame.draw.rect(screen, INVENTORY_BG, (inventory_x, inventory_y, inventory_width, inventory_height))
        for item in inventory_items:
            pygame.draw.rect(screen, INVENTORY_CELL_BG, item["rect"])
            pygame.draw.rect(screen, BLACK, item["rect"], 3)
            if item["image"]:
                img_x = item["rect"].x + (inventory_cell_size - item["image"].get_width()) // 2
                img_y = item["rect"].y + (inventory_cell_size - item["image"].get_height()) // 2
                screen.blit(item["image"], (img_x, img_y))
            if item["rect"].collidepoint(mouse_pos) and item["name"]:
                tooltip_text = font.render(seed_names.get(item["name"], item["name"]), True, WHITE)
                tooltip_rect = tooltip_text.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 10))
                pygame.draw.rect(screen, BLACK, (tooltip_rect.x - 2, tooltip_rect.y - 2, tooltip_rect.width + 4, tooltip_rect.height + 4))
                screen.blit(tooltip_text, tooltip_rect)
        
        pygame.draw.rect(screen, BUTTON_COLOR, prev_button)
        pygame.draw.rect(screen, BUTTON_COLOR, next_button)
        prev_text = font.render("<", True, WHITE)
        next_text = font.render(">", True, WHITE)
        screen.blit(prev_text, (prev_button.x + 20, prev_button.y + 2))
        screen.blit(next_text, (next_button.x + 20, next_button.y + 2))
        
        page_text = font.render(f"Trang {current_page + 1}/{total_pages}", True, WHITE)
        page_rect = page_text.get_rect(center=(inventory_x + inventory_width // 2, inventory_y + inventory_height - 15))
        screen.blit(page_text, page_rect)

    # Vẽ tooltip khi chuột hover vào feature
    for feature in features:
        if feature["rect"].collidepoint(mouse_pos):
            tooltip_text = font.render(feature["label"], True, WHITE)
            tooltip_rect = tooltip_text.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 10))
            pygame.draw.rect(screen, BLACK, (tooltip_rect.x - 2, tooltip_rect.y - 2, tooltip_rect.width + 4, tooltip_rect.height + 4))
            screen.blit(tooltip_text, tooltip_rect)

    # Kiểm tra và cập nhật con trỏ chuột
    cursor_changed = False
    if is_harvesting:
        pygame.mouse.set_visible(False)
        screen.blit(sickle_cursor, (mouse_pos[0], mouse_pos[1]))
    elif is_watering:
        pygame.mouse.set_visible(False)
        screen.blit(watering_can_cursor, (mouse_pos[0], mouse_pos[1]))
    else:
        pygame.mouse.set_visible(True)
        for plot in plots:
            if plot.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(hover_cursor)
                cursor_changed = True
                break

        for feature in features:
            if feature["rect"].collidepoint(mouse_pos):
                pygame.mouse.set_cursor(hover_cursor)
                cursor_changed = True
                break

        if show_inventory:
            inventory_items, total_pages = update_inventory_display()
            for item in inventory_items:
                if item["rect"].collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(hover_cursor)
                    cursor_changed = True
                    break
            if prev_button.collidepoint(mouse_pos) or next_button.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(hover_cursor)
                cursor_changed = True

        if not cursor_changed:
            pygame.mouse.set_cursor(default_cursor)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_inventory()
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Kiểm tra nhấn vào ô đất
            for index, plot in enumerate(plots):
                if plot.collidepoint(event.pos):
                    if is_harvesting and index in planted_seeds and planted_seeds[index]["stage"] == 3:
                        seed_type = planted_seeds[index]["seed"]
                        product = seed_to_product[seed_type]
                        player.inventory.add_item(product, 1)
                        del planted_seeds[index]
                        save_inventory()
                        print(f"Đã thu hoạch: {product}. Số lượng hiện tại: {player.inventory.get_item_quantity(product)}")
                    elif is_watering and index in planted_seeds:
                        planted_seeds[index]["last_watered"] = pygame.time.get_ticks()
                        print(f"Đã tưới nước cho cây tại ô {index}!")
                    elif index not in planted_seeds and selected_seed is not None and len(planted_seeds) < player.get_garden_slots():
                        if player.reduce_energy(ENERGY_COST) and player.inventory.remove_item(selected_seed, 1):
                            planted_seeds[index] = {
                                "seed": selected_seed,
                                "center_pos": plot.center,  # Lưu tâm điểm của ô đất
                                "stage": 1,
                                "time_planted": pygame.time.get_ticks(),
                                "last_watered": pygame.time.get_ticks()
                            }
                            save_inventory()
                            print(f"Đã trồng: {selected_seed}. Số lượng còn lại: {player.inventory.get_item_quantity(selected_seed)}")
                            selected_seed = None

            # Kiểm tra nhấn vào feature
            for feature in features:
                if feature["rect"].collidepoint(event.pos):
                    if feature["function"] == "plant_menu":
                        show_inventory = not show_inventory
                        is_harvesting = False
                        is_watering = False
                    elif feature["function"] == "water":
                        is_watering = not is_watering
                        is_harvesting = False
                        show_inventory = False
                        print(f"Chế độ tưới nước {'bật' if is_watering else 'tắt'}!")
                    elif feature["function"] == "remove":
                        print("Chức năng xóa được kích hoạt!")
                        is_harvesting = False
                        is_watering = False
                    elif feature["function"] == "harvest":
                        is_harvesting = not is_harvesting
                        is_watering = False
                        show_inventory = False
                        print(f"Chế độ thu hoạch {'bật' if is_harvesting else 'tắt'}!")

            # Kiểm tra nhấn vào ô trong inventory
            if show_inventory:
                inventory_items, total_pages = update_inventory_display()
                for item in inventory_items:
                    if item["rect"].collidepoint(event.pos) and item["name"]:
                        selected_seed = item["name"]
                        print(f"Đã chọn: {selected_seed}")
                        show_inventory = False
                
                if prev_button.collidepoint(event.pos) and current_page > 0:
                    current_page -= 1
                if next_button.collidepoint(event.pos) and current_page < total_pages - 1:
                    current_page += 1

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text_surface = font.render(f"({mouse_x}, {mouse_y})", True, WHITE)
    screen.blit(text_surface, (10, 10))
    pygame.display.flip()

pygame.quit()