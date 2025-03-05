import pygame
import sys
import json
sys.path.append("D:\\ĐHSG\\Python\\Project\\doAnPython\\src\\core")
from inventory import Inventory

# Khởi tạo pygame
pygame.init()

# Cấu hình màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nông trại")

# Load hình ảnh nền
farm_bg = pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\backgrounds\\khuvuon.png")
farm_bg = pygame.transform.scale(farm_bg, (WIDTH, HEIGHT))

# Load hình ảnh hạt giống và cây theo giai đoạn
plant_images = {
    "carrot_seed": {
        0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
        1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
        2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
        3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
    },
    # "cabbage_seed": {
    #     0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
    #     1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\cabbage1.png"), (40, 40)),
    #     2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\cabbage2.png"), (40, 40)),
    #     3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\cabbage3.png"), (40, 40)),
    # },
    # "tomato_seed": {
    #     0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
    #     1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\tomato1.png"), (40, 40)),
    #     2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\tomato2.png"), (40, 40)),
    #     3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\tomato3.png"), (40, 40)),
    # },
    # "potato_seed": {
    #     0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
    #     1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\potato1.png"), (40, 40)),
    #     2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\potato2.png"), (40, 40)),
    #     3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\potato3.png"), (40, 40)),
    # },
    # "energy_herb_seed": {
    #     0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
    #     1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\energy_herb1.png"), (40, 40)),
    #     2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\energy_herb2.png"), (40, 40)),
    #     3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\energy_herb3.png"), (40, 40)),
    # },
    # "rare_herb_seed": {
    #     0: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\icons\\seed.png"), (40, 40)),
    #     1: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\rare_herb1.png"), (40, 40)),
    #     2: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\rare_herb2.png"), (40, 40)),
    #     3: pygame.transform.scale(pygame.image.load("D:\\ĐHSG\\Python\\Project\\doAnPython\\assets\\images\\plants\\rare_herb3.png"), (40, 40)),
    # },
}

# Định dạng tên hạt giống đẹp hơn
seed_names = {
    "carrot_seed": "Carrot Seed",
    "cabbage_seed": "Cabbage Seed",
    "tomato_seed": "Tomato Seed",
    "potato_seed": "Potato Seed",
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
    "tomato_seed": "tomato",
    "potato_seed": "potato",
    "energy_herb_seed": "energy_herb",
    "rare_herb_seed": "rare_herb",
}

# Biến lưu trạng thái
planted_seeds = {}
mana = 200
MANA_COST = 20
font = pygame.font.Font(None, 24)
default_cursor = pygame.SYSTEM_CURSOR_ARROW
hover_cursor = pygame.SYSTEM_CURSOR_HAND
show_inventory = False
selected_seed = None
is_harvesting = False

# Thời gian mỗi giai đoạn (ms)
STAGE_DURATION = 5000

# Khởi tạo inventory từ inventory.py
game_inventory = Inventory()

# Hàm lưu inventory vào file
def save_inventory():
    with open("D:\\ĐHSG\\Python\\Project\\doAnPython\\src\\core\\inventory_data.json", "w") as f:
        json.dump(game_inventory.items, f)
    print("Đã lưu inventory vào file")

# Hàm tải inventory từ file
def load_inventory():
    try:
        with open("D:\\ĐHSG\\Python\\Project\\doAnPython\\src\\core\\inventory_data.json", "r") as f:
            game_inventory.items = json.load(f)
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
inventory_height = inventory_rows * inventory_cell_size + inventory_padding * 2
inventory_x = WIDTH // 2 - inventory_width // 2
inventory_y = HEIGHT // 2 - inventory_height // 2

# Hàm cập nhật inventory giao diện
def update_inventory_display():
    inventory_items = []
    seed_items = {k: v for k, v in game_inventory.get_all_items().items() if k.endswith("_seed")}
    for item_name, quantity in seed_items.items():
        for _ in range(quantity):
            inventory_items.append({"name": item_name, "image": plant_images[item_name][0]})
    
    total_slots = inventory_rows * inventory_cols
    while len(inventory_items) < total_slots:
        inventory_items.append({"name": None, "image": None})
    
    for i, item in enumerate(inventory_items[:total_slots]):
        row = i // inventory_cols
        col = i % inventory_cols
        item["rect"] = pygame.Rect(
            inventory_x + inventory_padding + col * inventory_cell_size,
            inventory_y + inventory_padding + row * inventory_cell_size,
            inventory_cell_size,
            inventory_cell_size
        )
    return inventory_items

# Hàm cập nhật giai đoạn cây trồng
def update_plant_stages():
    current_time = pygame.time.get_ticks()
    for index in list(planted_seeds.keys()):
        plant = planted_seeds[index]
        time_elapsed = current_time - plant["time_planted"]
        new_stage = min(3, time_elapsed // STAGE_DURATION)
        planted_seeds[index]["stage"] = new_stage

running = True
while running:
    screen.blit(farm_bg, (0, 0))

    # Cập nhật giai đoạn cây trồng
    update_plant_stages()

    # Vẽ ô đất
    for index, plot in enumerate(plots):
        pygame.draw.rect(screen, BROWN, plot, 3)
        if index in planted_seeds:
            seed_type = planted_seeds[index]["seed"]
            stage = planted_seeds[index]["stage"]
            seed_pos = planted_seeds[index]["pos"]
            screen.blit(plant_images[seed_type][stage], seed_pos)

    # Lấy vị trí chuột
    mouse_pos = pygame.mouse.get_pos()

    # Vẽ các nút feature
    for feature in features:
        pygame.draw.rect(screen, BLUE, feature["rect"], 3)

    # Vẽ thanh mana
    pygame.draw.rect(screen, WHITE, (20, 20, 204, 24))
    pygame.draw.rect(screen, BLUE, (22, 22, mana, 20))
    mana_text = font.render(f"Mana: {mana}/200", True, WHITE)
    screen.blit(mana_text, (20, 50))

    # Vẽ inventory nếu được kích hoạt
    if show_inventory:
        inventory_items = update_inventory_display()
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

    # Vẽ tooltip khi chuột hover vào feature
    for feature in features:
        if feature["rect"].collidepoint(mouse_pos):
            tooltip_text = font.render(feature["label"], True, WHITE)
            tooltip_rect = tooltip_text.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 10))
            pygame.draw.rect(screen, BLACK, (tooltip_rect.x - 2, tooltip_rect.y - 2, tooltip_rect.width + 4, tooltip_rect.height + 4))
            screen.blit(tooltip_text, tooltip_rect)

    # Kiểm tra con trỏ chuột
    cursor_changed = False
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
        inventory_items = update_inventory_display()
        for item in inventory_items:
            if item["rect"].collidepoint(mouse_pos):
                pygame.mouse.set_cursor(hover_cursor)
                cursor_changed = True
                break

    if not cursor_changed:
        pygame.mouse.set_cursor(default_cursor)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_inventory()  # Lưu inventory trước khi thoát
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Kiểm tra nhấn vào ô đất
            for index, plot in enumerate(plots):
                if plot.collidepoint(event.pos):
                    if is_harvesting and index in planted_seeds and planted_seeds[index]["stage"] == 3:
                        seed_type = planted_seeds[index]["seed"]
                        product = seed_to_product[seed_type]
                        game_inventory.add_item(product, 1)  # Cộng sản phẩm vào kho
                        del planted_seeds[index]
                        is_harvesting = False
                        save_inventory()  # Lưu sau khi thu hoạch
                        print(f"Đã thu hoạch: {product}. Số lượng hiện tại: {game_inventory.get_item_quantity(product)}")
                    elif mana >= MANA_COST and selected_seed is not None and index not in planted_seeds:
                        if game_inventory.remove_item(selected_seed, 1):  # Giảm hạt giống trong kho
                            planted_seeds[index] = {
                                "seed": selected_seed,
                                "pos": (plot.x + plot.width // 2 - 20, plot.y + plot.height // 2 - 20),
                                "stage": 0,
                                "time_planted": pygame.time.get_ticks()
                            }
                            mana -= MANA_COST
                            save_inventory()  # Lưu sau khi trồng
                            print(f"Đã trồng: {selected_seed}. Số lượng còn lại: {game_inventory.get_item_quantity(selected_seed)}")
                            selected_seed = None

            # Kiểm tra nhấn vào feature
            for feature in features:
                if feature["rect"].collidepoint(event.pos):
                    if feature["function"] == "plant_menu":
                        show_inventory = not show_inventory
                        is_harvesting = False
                    elif feature["function"] == "water":
                        print("Chức năng tưới nước được kích hoạt!")
                        is_harvesting = False
                    elif feature["function"] == "remove":
                        print("Chức năng xóa được kích hoạt!")
                        is_harvesting = False
                    elif feature["function"] == "harvest":
                        is_harvesting = True
                        show_inventory = False

            # Kiểm tra nhấn vào ô trong inventory
            if show_inventory:
                inventory_items = update_inventory_display()
                for item in inventory_items:
                    if item["rect"].collidepoint(event.pos) and item["name"]:
                        selected_seed = item["name"]
                        print(f"Đã chọn: {selected_seed}")
                        show_inventory = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text_surface = font.render(f"({mouse_x}, {mouse_y})", True, WHITE)
    screen.blit(text_surface, (10, 10))
    pygame.display.flip()

pygame.quit()