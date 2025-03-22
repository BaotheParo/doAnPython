import pygame
import sys
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(BASE_DIR, "src", "core"))

from inventory import Inventory
from player import Player
from time_system import TimeSystem

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Farm Game")

farm_bg = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "backgrounds", "khuvuon.png")).convert()
farm_bg = pygame.transform.scale(farm_bg, (WIDTH, HEIGHT))

# Load plant images
plant_images = {
    "carrot_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot.png")), (40, 40)),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), (50, 50)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot1.png")), (40, 40)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot2.png")), (70, 70)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), (50, 50)),
    },
    "cabbage_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai.png")), (40, 40)),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), (50, 50)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai1.png")), (40, 40)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai2.png")), (70, 70)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), (50, 50)),
    },
    "beetroot_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden.png")), (40, 40)),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), (50, 50)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden1.png")), (40, 40)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden2.png")), (70, 70)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), (50, 50)),
    },
    "pumpkin_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido.png")), (40, 40)),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), (50, 50)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido1.png")), (40, 40)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido2.png")), (70, 70)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), (50, 50)),
    },
    "energy_herb_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc.png")), (40, 40)),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), (50, 50)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc1.png")), (40, 40)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc2.png")), (70, 70)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), (50, 50)),
    },
    "rare_herb_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua.png")), (40, 40)),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), (50, 50)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua1.png")), (40, 40)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua2.png")), (70, 70)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), (50, 50)),
    },
}

warning_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "need_watering.png")), (20, 20))
lock_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "padlock.png")), (40, 40))

seed_names = {
    "carrot_seed": "Carrot Seed",
    "cabbage_seed": "Cabbage Seed",
    "beetroot_seed": "Beetroot Seed",
    "pumpkin_seed": "Pumpkin Seed",
    "energy_herb_seed": "Energy Herb Seed",
    "rare_herb_seed": "Rare Herb Seed",
}

# Colors
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INVENTORY_BG = (100, 70, 50)
INVENTORY_CELL_BG = (70, 50, 40)
BUTTON_COLOR = (150, 150, 150)
LOCKED_OVERLAY = (50, 50, 50, 150)

# Define plot rectangles
plots = [
    pygame.Rect(176, 330, 120, 50),  # Row 1
    pygame.Rect(326, 330, 80, 50),
    pygame.Rect(446, 330, 100, 50),
    pygame.Rect(583, 332, 120, 50),
    pygame.Rect(156, 409, 120, 50),  # Row 2
    pygame.Rect(312, 412, 85, 50),
    pygame.Rect(437, 409, 100, 50),
    pygame.Rect(588, 414, 90, 50)
]

# Define feature buttons
features = [
    {"rect": pygame.Rect(318, 35, 58, 78), "function": "plant_menu", "label": "Planting"},
    {"rect": pygame.Rect(386, 35, 58, 78), "function": "water", "label": "Watering"},
    {"rect": pygame.Rect(450, 35, 58, 78), "function": "remove", "label": "Remove"},
    {"rect": pygame.Rect(518, 35, 58, 78), "function": "harvest", "label": "Harvest"},
]

seed_to_product = {
    "carrot_seed": "carrot",
    "cabbage_seed": "cabbage",
    "beetroot_seed": "beetroot",
    "pumpkin_seed": "pumpkin",
    "energy_herb_seed": "energy_herb",
    "rare_herb_seed": "rare_herb",
}

player = Player()
player.load_game()  # Tải dữ liệu từ player_data.json
time_system = TimeSystem()
ENERGY_COST = 20
DEATH_TIME = 120000  # 2 minutes
UPGRADE_TIME = 60000  # 1 minute
WARNING_TIME = 30000  # 30 seconds

planted_seeds = {}  # Giữ nguyên biến toàn cục vì Player không quản lý planted_seeds
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 48)
default_cursor = pygame.SYSTEM_CURSOR_ARROW
hover_cursor = pygame.SYSTEM_CURSOR_HAND
sickle_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "ll.png")), (32, 32))
watering_can_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "watering_can.png")), (32, 32))
water_can_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "water-can.png")), (32, 32))
show_inventory = False
selected_seed = None
is_harvesting = False
is_watering = False
is_removing = False
current_page = 0
watering_animation = False
watering_animation_start = 0
WATERING_ANIMATION_DURATION = 500
FARM_DATA_FILE = os.path.join(BASE_DIR, "src", "core", "farm_data.json")

def save_farm_data():
    farm_data = {}
    for index, plant in planted_seeds.items():
        farm_data[str(index)] = {
            "seed": plant["seed"],
            "stage": plant["stage"],
            "remaining_upgrade_time": plant["remaining_upgrade_time"],
            "remaining_death_time": plant["remaining_death_time"],
            "center_pos": plant["center_pos"]
        }
    with open(FARM_DATA_FILE, "w") as f:
        json.dump(farm_data, f)

def load_farm_data():
    global planted_seeds
    try:
        with open(FARM_DATA_FILE, "r") as f:
            farm_data = json.load(f)
            for index, plant in farm_data.items():
                planted_seeds[int(index)] = {
                    "seed": plant["seed"],
                    "stage": plant["stage"],
                    "remaining_upgrade_time": plant["remaining_upgrade_time"],
                    "remaining_death_time": plant["remaining_death_time"],
                    "center_pos": tuple(plant["center_pos"])
                }
    except FileNotFoundError:
        planted_seeds = {}

load_farm_data()  # Tải dữ liệu cây trồng từ farm_data.json

inventory_rows = 2
inventory_cols = 5
inventory_cell_size = 50
inventory_padding = 10
inventory_width = inventory_cols * inventory_cell_size + inventory_padding * 2
inventory_height = inventory_rows * inventory_cell_size + inventory_padding * 2 + 40
inventory_x = WIDTH // 2 - inventory_width // 2
inventory_y = HEIGHT // 2 - inventory_height // 2
total_slots = inventory_rows * inventory_cols

prev_button = pygame.Rect(inventory_x + inventory_padding, inventory_y + inventory_height - 30, 50, 20)
next_button = pygame.Rect(inventory_x + inventory_width - inventory_padding - 50, inventory_y + inventory_height - 30, 50, 20)

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

def update_plant_stages(delta_time):
    for index in list(planted_seeds.keys()):
        plant = planted_seeds[index]
        if plant["stage"] >= 3:
            continue
        plant["remaining_death_time"] -= delta_time
        if plant["remaining_death_time"] <= 0 and plant["stage"] < 4:
            plant["stage"] = 4
            plant["remaining_upgrade_time"] = None
            print(f"Plant at plot {index} has died!")
            save_farm_data()
        if plant["remaining_upgrade_time"] is not None:
            plant["remaining_upgrade_time"] -= delta_time
            if plant["remaining_upgrade_time"] <= 0:
                plant["stage"] += 1
                if plant["stage"] < 3:
                    plant["remaining_upgrade_time"] = None
                    plant["remaining_death_time"] = DEATH_TIME
                else:
                    plant["remaining_upgrade_time"] = None
                    plant["remaining_death_time"] = None
                print(f"Plant at plot {index} upgraded to stage {plant['stage']}!")
                if plant["stage"] == 3:
                    print(f"Plant at plot {index} is fully grown!")
                save_farm_data()

running = True
clock = pygame.time.Clock()
last_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    delta_time = current_time - last_time
    last_time = current_time

    screen.blit(farm_bg, (0, 0))

    time_system.update(delta_time)
    update_plant_stages(delta_time)

    garden_slots = player.get_garden_slots()
    for index, plot in enumerate(plots):
        if index < garden_slots:
            if index in planted_seeds:
                seed_type = planted_seeds[index]["seed"]
                stage = planted_seeds[index]["stage"]
                center_pos = planted_seeds[index]["center_pos"]
                image = plant_images[seed_type][stage]
                img_x = center_pos[0] - image.get_width() // 2
                img_y = center_pos[1] - image.get_height() // 2
                screen.blit(image, (img_x, img_y))
                if stage < 3 and (planted_seeds[index]["remaining_upgrade_time"] is None or planted_seeds[index]["remaining_death_time"] <= WARNING_TIME):
                    if (current_time // 500) % 2 == 0:
                        warning_x = img_x + image.get_width() - warning_icon.get_width() // 2
                        warning_y = img_y - warning_icon.get_height() // 2
                        screen.blit(warning_icon, (warning_x, warning_y))
        else:
            overlay = pygame.Surface((plot.width, plot.height), pygame.SRCALPHA)
            overlay.fill(LOCKED_OVERLAY)
            screen.blit(overlay, (plot.x, plot.y))
            lock_alpha = 255 if (current_time // 500) % 2 == 0 else 200
            lock_surface = lock_icon.copy()
            lock_surface.set_alpha(lock_alpha)
            lock_x = plot.centerx - lock_surface.get_width() // 2
            lock_y = plot.centery - lock_surface.get_height() // 2
            screen.blit(lock_surface, (lock_x, lock_y))

    mouse_pos = pygame.mouse.get_pos()

    pygame.draw.rect(screen, WHITE, (20, 20, 104, 24))
    pygame.draw.rect(screen, BLUE, (22, 22, player.get_energy(), 20))
    energy_text = font.render(f"MANA: {player.get_energy()}/{player.max_energy}", True, WHITE)

    day_text = font.render(f"Date: {time_system.current_day}", True, WHITE)
    time_text = font.render(f"Time: {time_system.format_time(time_system.get_remaining_time())}", True, WHITE)
    day_night_text = font.render(f"Status: {time_system.get_time_of_day()}", True, WHITE)
    screen.blit(day_text, (WIDTH - 150, 10))
    screen.blit(time_text, (WIDTH - 150, 30))
    screen.blit(day_night_text, (WIDTH - 150, 50))

    if not time_system.is_day():
        night_overlay = pygame.Surface((WIDTH, HEIGHT))
        night_overlay.set_alpha(200)
        night_overlay.fill(BLACK)
        screen.blit(night_overlay, (0, 0))
        night_message = large_font.render("It's night, buddy! You can't be here!", True, WHITE)
        screen.blit(night_message, night_message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    else:
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

            pygame.draw.rect(screen, BUTTON_COLOR, prev_button)
            pygame.draw.rect(screen, BUTTON_COLOR, next_button)
            prev_text = font.render("<", True, WHITE)
            next_text = font.render(">", True, WHITE)
            screen.blit(prev_text, (prev_button.x + 20, prev_button.y + 2))
            screen.blit(next_text, (next_button.x + 20, next_button.y + 2))
            page_text = font.render(f"Page {current_page + 1}/{total_pages}", True, WHITE)
            screen.blit(page_text, page_text.get_rect(center=(inventory_x + inventory_width // 2, inventory_y + inventory_height - 15)))

        for feature in features:
            if feature["rect"].collidepoint(mouse_pos):
                tooltip_text = font.render(feature["label"], True, WHITE)
                tooltip_rect = tooltip_text.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 10))
                pygame.draw.rect(screen, BLACK, (tooltip_rect.x - 2, tooltip_rect.y - 2, tooltip_rect.width + 4, tooltip_rect.height + 4))
                screen.blit(tooltip_text, tooltip_rect)

    cursor_changed = False
    if time_system.is_day():
        if is_harvesting:
            pygame.mouse.set_visible(False)
            screen.blit(sickle_cursor, (mouse_pos[0], mouse_pos[1]))
        elif is_watering:
            pygame.mouse.set_visible(False)
            if watering_animation and (current_time - watering_animation_start < WATERING_ANIMATION_DURATION):
                screen.blit(watering_can_cursor, (mouse_pos[0], mouse_pos[1]))
            else:
                screen.blit(water_can_cursor, (mouse_pos[0], mouse_pos[1]))
                watering_animation = False
        elif is_removing:
            pygame.mouse.set_visible(False)
            screen.blit(sickle_cursor, (mouse_pos[0], mouse_pos[1]))
        else:
            pygame.mouse.set_visible(True)
            for plot in plots[:garden_slots]:
                if plot.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(hover_cursor)
                    cursor_changed = True
                    break
            for feature in features:
                if feature["rect"].collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(hover_cursor)
                    cursor_changed = True
                    break
            for plot in plots[garden_slots:]:
                if plot.collidepoint(mouse_pos):
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.save_game()  # Lưu dữ liệu Player khi thoát
            save_farm_data()    # Lưu dữ liệu cây trồng khi thoát
            time_system.save_time_data()
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and time_system.is_day():
            for index, plot in enumerate(plots[:garden_slots]):
                if plot.collidepoint(event.pos):
                    if is_harvesting and index in planted_seeds and planted_seeds[index]["stage"] == 3:
                        seed_type = planted_seeds[index]["seed"]
                        product = seed_to_product[seed_type]
                        player.inventory.add_item(product, 1)
                        del planted_seeds[index]
                        player.save_game()  # Lưu inventory sau khi thu hoạch
                        save_farm_data()    # Lưu trạng thái cây trồng
                    elif is_watering and index in planted_seeds and planted_seeds[index]["stage"] < 4:
                        plant = planted_seeds[index]
                        if plant["stage"] < 3 and plant["remaining_upgrade_time"] is None:
                            plant["remaining_upgrade_time"] = UPGRADE_TIME
                            plant["remaining_death_time"] = DEATH_TIME
                            watering_animation = True
                            watering_animation_start = current_time
                            save_farm_data()  # Lưu trạng thái cây trồng sau khi tưới
                            print(f"Watered plant at plot {index} in stage {plant['stage']}!")
                    elif is_removing and index in planted_seeds:
                        del planted_seeds[index]
                        save_farm_data()  # Lưu trạng thái cây trồng sau khi xóa
                    elif index not in planted_seeds and selected_seed is not None:
                        energy_success = player.reduce_energy(ENERGY_COST)
                        inventory_success = player.inventory.remove_item(selected_seed, 1)
                        if energy_success and inventory_success:
                            planted_seeds[index] = {
                                "seed": selected_seed,
                                "stage": 1,
                                "remaining_upgrade_time": None,
                                "remaining_death_time": DEATH_TIME,
                                "center_pos": list(plot.center)
                            }
                            player.save_game()  # Lưu energy và inventory sau khi trồng
                            save_farm_data()    # Lưu trạng thái cây trồng
                            print(f"Đã trồng {selected_seed} tại ô {index}")
                            selected_seed = None
                        else:
                            if not energy_success:
                                print("Không đủ năng lượng để trồng cây!")
                            if not inventory_success:
                                print(f"Không đủ {selected_seed} trong kho!")

            for feature in features:
                if feature["rect"].collidepoint(event.pos):
                    if feature["function"] == "plant_menu":
                        show_inventory = not show_inventory
                        is_harvesting = is_watering = is_removing = False
                    elif feature["function"] == "water":
                        is_watering = not is_watering
                        is_harvesting = is_removing = show_inventory = False
                    elif feature["function"] == "remove":
                        is_removing = not is_removing
                        is_harvesting = is_watering = show_inventory = False
                    elif feature["function"] == "harvest":
                        is_harvesting = not is_harvesting
                        is_watering = is_removing = show_inventory = False

            if show_inventory:
                inventory_items, total_pages = update_inventory_display()
                for item in inventory_items:
                    if item["rect"].collidepoint(event.pos) and item["name"]:
                        selected_seed = item["name"]
                        show_inventory = False
                if prev_button.collidepoint(event.pos) and current_page > 0:
                    current_page -= 1
                if next_button.collidepoint(event.pos) and current_page < total_pages - 1:
                    current_page += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()