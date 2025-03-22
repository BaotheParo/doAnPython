import pygame
import sys
import json
import os
import math  # Dùng cho hiệu ứng xoay và nhấp nháy

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(BASE_DIR, "src", "core"))
sys.path.append(os.path.join(BASE_DIR, "src", "scenes"))

from inventory import Inventory
from player import Player
from time_system import TimeSystem
import fishing

pygame.init()

# Định nghĩa kích thước và tỉ lệ
WIDTH, HEIGHT = 1280, 720
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 800, 600
SCALE_X = WIDTH / ORIGINAL_WIDTH
SCALE_Y = HEIGHT / ORIGINAL_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Farm Game")

farm_bg = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "backgrounds", "khuvuon.png")).convert()
farm_bg = pygame.transform.scale(farm_bg, (WIDTH, HEIGHT))

# Hàm hỗ trợ điều chỉnh kích thước
def scale_size(original_size):
    return (int(original_size[0] * SCALE_X), int(original_size[1] * SCALE_Y))

# Load plant images
plant_images = {
    "carrot_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot.png")), scale_size((40, 40))),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), scale_size((50, 50))),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot1.png")), scale_size((40, 40))),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot2.png")), scale_size((70, 70))),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), scale_size((50, 50))),
    },
    "cabbage_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai.png")), scale_size((40, 40))),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), scale_size((50, 50))),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai1.png")), scale_size((40, 40))),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai2.png")), scale_size((70, 70))),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), scale_size((50, 50))),
    },
    "beetroot_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden.png")), scale_size((40, 40))),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), scale_size((50, 50))),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden1.png")), scale_size((40, 40))),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden2.png")), scale_size((70, 70))),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), scale_size((50, 50))),
    },
    "pumpkin_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido.png")), scale_size((40, 40))),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), scale_size((50, 50))),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido1.png")), scale_size((40, 40))),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido2.png")), scale_size((70, 70))),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), scale_size((50, 50))),
    },
    "energy_herb_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc.png")), scale_size((40, 40))),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), scale_size((50, 50))),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc1.png")), scale_size((40, 40))),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc2.png")), scale_size((70, 70))),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), scale_size((50, 50))),
    },
    "rare_herb_seed": {
        0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua.png")), scale_size((40, 40))),
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), scale_size((50, 50))),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua1.png")), scale_size((40, 40))),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua2.png")), scale_size((70, 70))),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), scale_size((50, 50))),
    },
}

warning_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "need_watering.png")), scale_size((20, 20)))
lock_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "padlock.png")), scale_size((50, 50)))  # Kích thước lớn hơn
back_button_image = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "icon-quaylai.png")), scale_size((40, 40)))

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
BLUE = (0, 191, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INVENTORY_BG = (100, 70, 50)
INVENTORY_CELL_BG = (70, 50, 40)
BUTTON_COLOR = (150, 150, 150)
GLOW_COLOR = (255, 215, 0, 120)  # Vàng kim loại cho hiệu ứng phát sáng
PARTICLE_COLOR = (255, 255, 0, 180)  # Hạt vàng sáng

# Define plot rectangles
plots = [
    pygame.Rect(176 * SCALE_X, 330 * SCALE_Y, 120 * SCALE_X, 50 * SCALE_Y),  # Row 1
    pygame.Rect(326 * SCALE_X, 330 * SCALE_Y, 80 * SCALE_X, 50 * SCALE_Y),
    pygame.Rect(446 * SCALE_X, 330 * SCALE_Y, 100 * SCALE_X, 50 * SCALE_Y),
    pygame.Rect(583 * SCALE_X, 332 * SCALE_Y, 120 * SCALE_X, 50 * SCALE_Y),
    pygame.Rect(156 * SCALE_X, 409 * SCALE_Y, 120 * SCALE_X, 50 * SCALE_Y),  # Row 2
    pygame.Rect(312 * SCALE_X, 412 * SCALE_Y, 85 * SCALE_X, 50 * SCALE_Y),
    pygame.Rect(437 * SCALE_X, 409 * SCALE_Y, 100 * SCALE_X, 50 * SCALE_Y),
    pygame.Rect(588 * SCALE_X, 414 * SCALE_Y, 90 * SCALE_X, 50 * SCALE_Y)
]

# Define feature buttons
features = [
    {"rect": pygame.Rect(318 * SCALE_X, 35 * SCALE_Y, 58 * SCALE_X, 78 * SCALE_Y), "function": "plant_menu", "label": "Planting"},
    {"rect": pygame.Rect(386 * SCALE_X, 35 * SCALE_Y, 58 * SCALE_X, 78 * SCALE_Y), "function": "water", "label": "Watering"},
    {"rect": pygame.Rect(450 * SCALE_X, 35 * SCALE_Y, 58 * SCALE_X, 78 * SCALE_Y), "function": "remove", "label": "Remove"},
    {"rect": pygame.Rect(518 * SCALE_X, 35 * SCALE_Y, 58 * SCALE_X, 78 * SCALE_Y), "function": "harvest", "label": "Harvest"},
]

# Define back button
back_button = pygame.Rect(10 * SCALE_X, 10 * SCALE_Y, 40 * SCALE_X, 40 * SCALE_Y)

# Define mana bar
MANA_BAR_WIDTH = int(600 * SCALE_X)
MANA_BAR_HEIGHT = int(30 * SCALE_Y)
MANA_BAR_X = (WIDTH - MANA_BAR_WIDTH) // 2
MANA_BAR_Y = HEIGHT - int(50 * SCALE_Y)

seed_to_product = {
    "carrot_seed": "carrot",
    "cabbage_seed": "cabbage",
    "beetroot_seed": "beetroot",
    "pumpkin_seed": "pumpkin",
    "energy_herb_seed": "energy_herb",
    "rare_herb_seed": "rare_herb",
}

player = Player()
player.load_game()
time_system = TimeSystem()
ENERGY_COST = 20
DEATH_TIME = 120000  # 2 minutes
UPGRADE_TIME = 60000  # 1 minute
WARNING_TIME = 30000  # 30 seconds

planted_seeds = {}
font = pygame.font.Font(None, int(24 * SCALE_X))
large_font = pygame.font.Font(None, int(48 * SCALE_X))
default_cursor = pygame.SYSTEM_CURSOR_ARROW
hover_cursor = pygame.SYSTEM_CURSOR_HAND
sickle_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "ll.png")), scale_size((32, 32)))
watering_can_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "watering_can.png")), scale_size((32, 32)))
water_can_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "water-can.png")), scale_size((32, 32)))
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

# Danh sách hạt cho hiệu ứng
particles = []

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

load_farm_data()

inventory_rows = 2
inventory_cols = 5
inventory_cell_size = int(50 * SCALE_X)
inventory_padding = int(10 * SCALE_X)
inventory_width = inventory_cols * inventory_cell_size + inventory_padding * 2
inventory_height = inventory_rows * inventory_cell_size + inventory_padding * 2 + int(40 * SCALE_Y)
inventory_x = WIDTH // 2 - inventory_width // 2
inventory_y = HEIGHT // 2 - inventory_height // 2
total_slots = inventory_rows * inventory_cols

prev_button = pygame.Rect(inventory_x + inventory_padding, inventory_y + inventory_height - int(30 * SCALE_Y), int(50 * SCALE_X), int(20 * SCALE_Y))
next_button = pygame.Rect(inventory_x + inventory_width - inventory_padding - int(50 * SCALE_X), inventory_y + inventory_height - int(30 * SCALE_Y), int(50 * SCALE_X), int(20 * SCALE_Y))

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

def update_particles(delta_time):
    global particles
    for particle in particles[:]:
        particle["x"] += particle["vx"] * delta_time / 1000
        particle["y"] += particle["vy"] * delta_time / 1000
        particle["life"] -= delta_time
        if particle["life"] <= 0:
            particles.remove(particle)

def add_particle(x, y):
    import random
    particles.append({
        "x": x,
        "y": y,
        "vx": random.uniform(-50, 50),
        "vy": random.uniform(-50, 50),
        "life": random.uniform(500, 1000)  # Thời gian sống của hạt (ms)
    })

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
    update_particles(delta_time)

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
            # Hiệu ứng hiện đại cho ô đất bị khóa
            lock_x = plot.centerx - lock_icon.get_width() // 2
            lock_y = plot.centery - lock_icon.get_height() // 2
            
            # Hiệu ứng phát sáng nhấp nháy
            glow_surface = pygame.Surface((lock_icon.get_width() + 30, lock_icon.get_height() + 30), pygame.SRCALPHA)
            glow_radius = int(35 * SCALE_X * (1 + 0.2 * math.sin(current_time / 500)))
            pygame.draw.circle(glow_surface, GLOW_COLOR, (glow_surface.get_width() // 2, glow_surface.get_height() // 2), glow_radius)
            screen.blit(glow_surface, (lock_x - 15, lock_y - 15))
            
            # Biểu tượng khóa xoay nhẹ
            angle = math.sin(current_time / 1000) * 10  # Xoay ±10 độ
            rotated_lock = pygame.transform.rotate(lock_icon, angle)
            lock_rect = rotated_lock.get_rect(center=(plot.centerx, plot.centery))
            screen.blit(rotated_lock, lock_rect.topleft)
            
            # Hiệu ứng hạt (particle effect)
            if current_time % 200 < delta_time:  # Tạo hạt mỗi 200ms
                add_particle(plot.centerx, plot.centery)
            for particle in particles:
                pygame.draw.circle(screen, PARTICLE_COLOR, (int(particle["x"]), int(particle["y"])), 3)
                particle["alpha"] = int(255 * (particle["life"] / 1000))
                particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, (*PARTICLE_COLOR[:3], particle["alpha"]), (3, 3), 3)
                screen.blit(particle_surface, (int(particle["x"]) - 3, int(particle["y"]) - 3))

    # Vẽ nút quay lại
    screen.blit(back_button_image, (back_button.x, back_button.y))

    mouse_pos = pygame.mouse.get_pos()

    # Vẽ thanh mana
    pygame.draw.rect(screen, BLACK, (MANA_BAR_X - 5, MANA_BAR_Y - 5, MANA_BAR_WIDTH + 10, MANA_BAR_HEIGHT + 10), border_radius=5)
    pygame.draw.rect(screen, WHITE, (MANA_BAR_X, MANA_BAR_Y, MANA_BAR_WIDTH, MANA_BAR_HEIGHT), border_radius=5)
    mana_width = (player.get_energy() / player.max_energy) * (MANA_BAR_WIDTH - 4)
    pygame.draw.rect(screen, BLUE, (MANA_BAR_X + 2, MANA_BAR_Y + 2, mana_width, MANA_BAR_HEIGHT - 4), border_radius=5)
    energy_text = font.render(f"MANA: {player.get_energy()}/{player.max_energy}", True, BLACK)
    screen.blit(energy_text, (MANA_BAR_X + (MANA_BAR_WIDTH - energy_text.get_width()) // 2, MANA_BAR_Y + (MANA_BAR_HEIGHT - energy_text.get_height()) // 2))

    # Vẽ thông tin ngày giờ
    day_text = font.render(f"Date: {time_system.current_day}", True, WHITE)
    time_text = font.render(f"Time: {time_system.format_time(time_system.get_remaining_time())}", True, WHITE)
    day_night_text = font.render(f"Status: {time_system.get_time_of_day()}", True, WHITE)
    screen.blit(day_text, (WIDTH - 150 * SCALE_X, 10 * SCALE_Y))
    screen.blit(time_text, (WIDTH - 150 * SCALE_X, 30 * SCALE_Y))
    screen.blit(day_night_text, (WIDTH - 150 * SCALE_X, 50 * SCALE_Y))

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
            pygame.draw.rect(screen, INVENTORY_BG, (inventory_x, inventory_y, inventory_width, inventory_height), border_radius=10)
            for item in inventory_items:
                pygame.draw.rect(screen, INVENTORY_CELL_BG, item["rect"], border_radius=5)
                pygame.draw.rect(screen, BLACK, item["rect"], 3, border_radius=5)
                if item["image"]:
                    img_x = item["rect"].x + (inventory_cell_size - item["image"].get_width()) // 2
                    img_y = item["rect"].y + (inventory_cell_size - item["image"].get_height()) // 2
                    screen.blit(item["image"], (img_x, img_y))

            pygame.draw.rect(screen, BUTTON_COLOR, prev_button, border_radius=5)
            pygame.draw.rect(screen, BUTTON_COLOR, next_button, border_radius=5)
            prev_text = font.render("<", True, WHITE)
            next_text = font.render(">", True, WHITE)
            screen.blit(prev_text, (prev_button.x + 20 * SCALE_X, prev_button.y + 2 * SCALE_Y))
            screen.blit(next_text, (next_button.x + 20 * SCALE_X, next_button.y + 2 * SCALE_Y))
            page_text = font.render(f"Page {current_page + 1}/{total_pages}", True, WHITE)
            screen.blit(page_text, page_text.get_rect(center=(inventory_x + inventory_width // 2, inventory_y + inventory_height - 15 * SCALE_Y)))

        for feature in features:
            if feature["rect"].collidepoint(mouse_pos):
                tooltip_text = font.render(feature["label"], True, WHITE)
                tooltip_rect = tooltip_text.get_rect(topleft=(mouse_pos[0] + 10 * SCALE_X, mouse_pos[1] + 10 * SCALE_Y))
                pygame.draw.rect(screen, BLACK, (tooltip_rect.x - 2 * SCALE_X, tooltip_rect.y - 2 * SCALE_Y, tooltip_rect.width + 4 * SCALE_X, tooltip_rect.height + 4 * SCALE_Y), border_radius=5)
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
            if back_button.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(hover_cursor)
                cursor_changed = True
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
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if back_button.collidepoint(event.pos):
                from src.core.ui import SettingsUI
                pygame.quit()
                pygame.init()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                settings_ui = SettingsUI(screen, player, time_system, planted_seeds)
                fishing_scene = fishing.FishingScene(player, time_system, screen, settings_ui)
                fishing_scene.run()
                sys.exit()

            if time_system.is_day():
                for index, plot in enumerate(plots[:garden_slots]):
                    if plot.collidepoint(event.pos):
                        if is_harvesting and index in planted_seeds and planted_seeds[index]["stage"] == 3:
                            seed_type = planted_seeds[index]["seed"]
                            product = seed_to_product[seed_type]
                            player.inventory.add_item(product, 1)
                            del planted_seeds[index]
                        elif is_watering and index in planted_seeds and planted_seeds[index]["stage"] < 4:
                            plant = planted_seeds[index]
                            if plant["stage"] < 3 and plant["remaining_upgrade_time"] is None:
                                plant["remaining_upgrade_time"] = UPGRADE_TIME
                                plant["remaining_death_time"] = DEATH_TIME
                                watering_animation = True
                                watering_animation_start = current_time
                                print(f"Watered plant at plot {index} in stage {plant['stage']}!")
                        elif is_removing and index in planted_seeds:
                            del planted_seeds[index]
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