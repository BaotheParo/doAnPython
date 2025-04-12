import pygame
import sys
import json
import os
import math
import random

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(BASE_DIR, "src", "core"))
sys.path.append(os.path.join(BASE_DIR, "src", "scenes"))

from inventory import Inventory
from player import Player
from time_system import TimeSystem

class FarmGame:
    def __init__(self, player=None, time_system=None, planted_seeds=None):
        pygame.init()
        
        # Screen settings
        self.WIDTH, self.HEIGHT = 1280, 720
        self.ORIGINAL_WIDTH, self.ORIGINAL_HEIGHT = 800, 600
        self.SCALE_X = self.WIDTH / self.ORIGINAL_WIDTH
        self.SCALE_Y = self.HEIGHT / self.ORIGINAL_HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Farm Game")

        # Load background
        self.farm_bg = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "backgrounds", "khuvuon.png")).convert()
        self.farm_bg = pygame.transform.scale(self.farm_bg, (self.WIDTH, self.HEIGHT))

        # Colors
        self.BROWN = (139, 69, 19)
        self.BLUE = (0, 191, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.INVENTORY_BG = (100, 70, 50)
        self.INVENTORY_CELL_BG = (70, 50, 40)
        self.BUTTON_COLOR = (150, 150, 150)
        self.GLOW_COLOR = (255, 215, 0, 120)
        self.PARTICLE_COLOR = (255, 255, 0, 180)
        self.WARNING_COLOR = (255, 0, 0)  # Màu đỏ cho thông báo

        # Game constants
        self.ENERGY_COST = 20
        self.DEATH_TIME = 120000  # 2 minutes
        self.UPGRADE_TIME = 60000  # 1 minute
        self.WARNING_TIME = 30000  # 30 seconds
        self.WATERING_ANIMATION_DURATION = 500
        self.MESSAGE_DURATION = 2000  # Thời gian hiển thị thông báo (2 giây)
        self.FARM_DATA_FILE = os.path.join(BASE_DIR, "src", "core", "farm_data.json")

        # Initialize game objects
        self.player = player if player else Player()
        if not player:  # Chỉ load nếu không truyền player từ ngoài vào
            self.player.load_game()
        self.time_system = time_system if time_system else TimeSystem()
        self.planted_seeds = self.time_system.get_plants()  # Lấy từ TimeSystem
        if planted_seeds is not None:
            self.time_system.load_plants(planted_seeds)  # Nếu có planted_seeds truyền vào, cập nhật vào TimeSystem

        # Khởi tạo danh sách particles
        self.particles = []  # Danh sách hạt hiệu ứng

        # UI settings
        self.font = pygame.font.Font(None, int(24 * self.SCALE_X))
        self.large_font = pygame.font.Font(None, int(48 * self.SCALE_X))
        self.default_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.hover_cursor = pygame.SYSTEM_CURSOR_HAND
        self.load_images_and_cursors()

        # Game state
        self.show_inventory = False
        self.selected_seed = None
        self.is_harvesting = False
        self.is_watering = False
        self.is_removing = False
        self.current_page = 0
        self.watering_animation = False
        self.watering_animation_start = 0
        self.message = None  # Thông báo
        self.message_timer = 0  # Thời gian còn lại để hiển thị thông báo

        # Define UI elements
        self.define_plots_and_features()
        self.define_inventory_ui()

        # Load initial data if not provided
        if planted_seeds is None:
            self.load_farm_data()

        # Clock
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()

    def scale_size(self, original_size):
        return (int(original_size[0] * self.SCALE_X), int(original_size[1] * self.SCALE_Y))

    def load_images_and_cursors(self):
        self.plant_images = {
            "carrot_seed": {
                0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot.png")), self.scale_size((40, 40))),
                1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), self.scale_size((50, 50))),
                2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot1.png")), self.scale_size((40, 40))),
                3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "carot2.png")), self.scale_size((70, 70))),
                4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), self.scale_size((50, 50))),
            },
            "cabbage_seed": {
                0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai.png")), self.scale_size((40, 40))),
                1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), self.scale_size((50, 50))),
                2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai1.png")), self.scale_size((40, 40))),
                3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bapcai2.png")), self.scale_size((70, 70))),
                4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), self.scale_size((50, 50))),
            },
            "beetroot_seed": {
                0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden.png")), self.scale_size((40, 40))),
                1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), self.scale_size((50, 50))),
                2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden1.png")), self.scale_size((40, 40))),
                3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "cuden2.png")), self.scale_size((70, 70))),
                4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), self.scale_size((50, 50))),
            },
            "pumpkin_seed": {
                0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido.png")), self.scale_size((40, 40))),
                1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), self.scale_size((50, 50))),
                2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido1.png")), self.scale_size((40, 40))),
                3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "bido2.png")), self.scale_size((70, 70))),
                4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), self.scale_size((50, 50))),
            },
            "energy_herb_seed": {
                0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc.png")), self.scale_size((40, 40))),
                1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), self.scale_size((50, 50))),
                2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc1.png")), self.scale_size((40, 40))),
                3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "thaomoc2.png")), self.scale_size((70, 70))),
                4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), self.scale_size((50, 50))),
            },
            "rare_herb_seed": {
                0: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua.png")), self.scale_size((40, 40))),
                1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "seed.png")), self.scale_size((50, 50))),
                2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua1.png")), self.scale_size((40, 40))),
                3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "lua2.png")), self.scale_size((70, 70))),
                4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "plants", "caychet.png")), self.scale_size((50, 50))),
            },
        }

        self.warning_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "need_watering.png")), self.scale_size((20, 20)))
        self.lock_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "padlock.png")), self.scale_size((50, 50)))
        self.back_button_image = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "icon-quaylai.png")), self.scale_size((40, 40)))
        self.sickle_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "ll.png")), self.scale_size((50, 50)))
        self.watering_can_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "watering_can.png")), self.scale_size((60, 60)))
        self.water_can_cursor = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "water-can.png")), self.scale_size((50, 50)))

        # Thêm icon cho cây chết và cây cần thu hoạch
        self.dead_plant_icon = pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "dead_plant.png")),
            self.scale_size((30, 30))
        )
        self.ready_harvest_icon = pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "icons", "ll.png")),
            self.scale_size((30, 30))
        )

        self.seed_names = {
            "carrot_seed": "Carrot Seed",
            "cabbage_seed": "Cabbage Seed",
            "beetroot_seed": "Beetroot Seed",
            "pumpkin_seed": "Pumpkin Seed",
            "energy_herb_seed": "Energy Herb Seed",
            "rare_herb_seed": "Rare Herb Seed",
        }

        self.seed_to_product = {
            "carrot_seed": "carrot",
            "cabbage_seed": "cabbage",
            "beetroot_seed": "beetroot",
            "pumpkin_seed": "pumpkin",
            "energy_herb_seed": "energy_herb",
            "rare_herb_seed": "rare_herb",
        }

    def define_plots_and_features(self):
        self.plots = [
            pygame.Rect(176 * self.SCALE_X, 330 * self.SCALE_Y, 120 * self.SCALE_X, 50 * self.SCALE_Y),  # Row 1
            pygame.Rect(326 * self.SCALE_X, 330 * self.SCALE_Y, 80 * self.SCALE_X, 50 * self.SCALE_Y),
            pygame.Rect(446 * self.SCALE_X, 330 * self.SCALE_Y, 100 * self.SCALE_X, 50 * self.SCALE_Y),
            pygame.Rect(583 * self.SCALE_X, 332 * self.SCALE_Y, 120 * self.SCALE_X, 50 * self.SCALE_Y),
            pygame.Rect(156 * self.SCALE_X, 409 * self.SCALE_Y, 120 * self.SCALE_X, 50 * self.SCALE_Y),  # Row 2
            pygame.Rect(312 * self.SCALE_X, 412 * self.SCALE_Y, 85 * self.SCALE_X, 50 * self.SCALE_Y),
            pygame.Rect(437 * self.SCALE_X, 409 * self.SCALE_Y, 100 * self.SCALE_X, 50 * self.SCALE_Y),
            pygame.Rect(588 * self.SCALE_X, 414 * self.SCALE_Y, 90 * self.SCALE_X, 50 * self.SCALE_Y)
        ]

        self.features = [
            {"rect": pygame.Rect(318 * self.SCALE_X, 35 * self.SCALE_Y, 58 * self.SCALE_X, 78 * self.SCALE_Y), "function": "plant_menu", "label": "Planting"},
            {"rect": pygame.Rect(386 * self.SCALE_X, 35 * self.SCALE_Y, 58 * self.SCALE_X, 78 * self.SCALE_Y), "function": "water", "label": "Watering"},
            {"rect": pygame.Rect(450 * self.SCALE_X, 35 * self.SCALE_Y, 58 * self.SCALE_X, 78 * self.SCALE_Y), "function": "remove", "label": "Remove"},
            {"rect": pygame.Rect(518 * self.SCALE_X, 35 * self.SCALE_Y, 58 * self.SCALE_X, 78 * self.SCALE_Y), "function": "harvest", "label": "Harvest"},
        ]

        self.back_button = pygame.Rect(10 * self.SCALE_X, 10 * self.SCALE_Y, 40 * self.SCALE_X, 40 * self.SCALE_Y)
        self.MANA_BAR_WIDTH = int(600 * self.SCALE_X)
        self.MANA_BAR_HEIGHT = int(30 * self.SCALE_Y)
        self.MANA_BAR_X = (self.WIDTH - self.MANA_BAR_WIDTH) // 2
        self.MANA_BAR_Y = self.HEIGHT - int(50 * self.SCALE_Y)

    def define_inventory_ui(self):
        self.inventory_rows = 2
        self.inventory_cols = 5
        self.inventory_cell_size = int(50 * self.SCALE_X)
        self.inventory_padding = int(10 * self.SCALE_X)
        self.inventory_width = self.inventory_cols * self.inventory_cell_size + self.inventory_padding * 2
        self.inventory_height = self.inventory_rows * self.inventory_cell_size + self.inventory_padding * 2 + int(40 * self.SCALE_Y)
        self.inventory_x = self.WIDTH // 2 - self.inventory_width // 2
        self.inventory_y = self.HEIGHT // 2 - self.inventory_height // 2
        self.total_slots = self.inventory_rows * self.inventory_cols
        self.prev_button = pygame.Rect(self.inventory_x + self.inventory_padding, self.inventory_y + self.inventory_height - int(30 * self.SCALE_Y), int(50 * self.SCALE_X), int(20 * self.SCALE_Y))
        self.next_button = pygame.Rect(self.inventory_x + self.inventory_width - self.inventory_padding - int(50 * self.SCALE_X), self.inventory_y + self.inventory_height - int(30 * self.SCALE_Y), int(50 * self.SCALE_X), int(20 * self.SCALE_Y))

    def save_farm_data(self):
        farm_data = {str(index): {
            "seed": plant["seed"],
            "stage": plant["stage"],
            "remaining_upgrade_time": plant["remaining_upgrade_time"],
            "remaining_death_time": plant["remaining_death_time"],
            "center_pos": plant["center_pos"]
        } for index, plant in self.time_system.get_plants().items()}
        with open(self.FARM_DATA_FILE, "w") as f:
            json.dump(farm_data, f)

    def load_farm_data(self):
        try:
            with open(self.FARM_DATA_FILE, "r") as f:
                farm_data = json.load(f)
                self.time_system.load_plants({int(index): {
                    "seed": plant["seed"],
                    "stage": plant["stage"],
                    "remaining_upgrade_time": plant["remaining_upgrade_time"],
                    "remaining_death_time": plant["remaining_death_time"],
                    "center_pos": tuple(plant["center_pos"])
                } for index, plant in farm_data.items()})
        except FileNotFoundError:
            self.time_system.load_plants({})

    def update_inventory_display(self):
        inventory_items = []
        seed_items = {k: v for k, v in self.player.inventory.get_all_items().items() if k.endswith("_seed")}
        for item_name, quantity in seed_items.items():
            for _ in range(quantity):
                inventory_items.append({"name": item_name, "image": self.plant_images[item_name][0]})

        total_items = len(inventory_items)
        total_pages = (total_items + self.total_slots - 1) // self.total_slots
        self.current_page = max(0, min(self.current_page, total_pages - 1)) if total_pages > 0 else 0
        start_index = self.current_page * self.total_slots
        end_index = min(start_index + self.total_slots, total_items)
        visible_items = inventory_items[start_index:end_index]

        while len(visible_items) < self.total_slots:
            visible_items.append({"name": None, "image": None})

        for i, item in enumerate(visible_items):
            row = i // self.inventory_cols
            col = i % self.inventory_cols
            item["rect"] = pygame.Rect(
                self.inventory_x + self.inventory_padding + col * self.inventory_cell_size,
                self.inventory_y + self.inventory_padding + row * self.inventory_cell_size,
                self.inventory_cell_size,
                self.inventory_cell_size
            )
        return visible_items, total_pages

    def update_particles(self, delta_time):
        for particle in self.particles[:]:
            particle["x"] += particle["vx"] * delta_time / 1000
            particle["y"] += particle["vy"] * delta_time / 1000
            particle["life"] -= delta_time
            if particle["life"] <= 0:
                self.particles.remove(particle)

    def add_particle(self, x, y):
        self.particles.append({
            "x": x,
            "y": y,
            "vx": random.uniform(-50, 50),
            "vy": random.uniform(-50, 50),
            "life": random.uniform(500, 1000)
        })

    def get_blinking_alpha(self, current_time, period=1000):
        """
        Tính toán giá trị alpha (0-255) để tạo hiệu ứng nhấp nháy.
        period: Chu kỳ nhấp nháy (ms), mặc định 1 giây.
        """
        alpha = 255 * (0.5 + 0.5 * math.sin(2 * math.pi * current_time / period))
        return int(alpha)

    def draw(self, current_time):
        self.screen.blit(self.farm_bg, (0, 0))
        garden_slots = self.player.get_garden_slots()
        self.planted_seeds = self.time_system.get_plants()  # Cập nhật planted_seeds từ TimeSystem
        
        for index, plot in enumerate(self.plots):
            if index < garden_slots:
                if index in self.planted_seeds:
                    seed_type = self.planted_seeds[index]["seed"]
                    stage = self.planted_seeds[index]["stage"]
                    center_pos = self.planted_seeds[index]["center_pos"]
                    image = self.plant_images[seed_type][stage]
                    img_x = center_pos[0] - image.get_width() // 2
                    img_y = center_pos[1] - image.get_height() // 2
                    self.screen.blit(image, (img_x, img_y))

                    # Hiệu ứng nhấp nháy cho cây cần tưới
                    if stage < 3 and (self.planted_seeds[index]["remaining_upgrade_time"] is None or self.planted_seeds[index]["remaining_death_time"] <= self.WARNING_TIME):
                        if (current_time // 500) % 2 == 0:
                            warning_x = img_x + image.get_width() - self.warning_icon.get_width() // 2
                            warning_y = img_y - self.warning_icon.get_height() // 2
                            self.screen.blit(self.warning_icon, (warning_x, warning_y))

                    # Hiệu ứng nhấp nháy cho cây chết (stage = 4)
                    if stage == 4:
                        dead_icon_surface = pygame.Surface(self.dead_plant_icon.get_size(), pygame.SRCALPHA)
                        alpha = self.get_blinking_alpha(current_time)
                        dead_icon_surface.blit(self.dead_plant_icon, (0, 0))
                        dead_icon_surface.set_alpha(alpha)
                        dead_icon_x = img_x + image.get_width() // 2
                        dead_icon_y = img_y - self.dead_plant_icon.get_height() // 2
                        self.screen.blit(dead_icon_surface, (dead_icon_x, dead_icon_y))

                    # Hiệu ứng nhấp nháy cho cây cần thu hoạch (stage = 3)
                    if stage == 3:
                        harvest_icon_surface = pygame.Surface(self.ready_harvest_icon.get_size(), pygame.SRCALPHA)
                        alpha = self.get_blinking_alpha(current_time)
                        harvest_icon_surface.blit(self.ready_harvest_icon, (0, 0))
                        harvest_icon_surface.set_alpha(alpha)
                        harvest_icon_x = img_x + image.get_width() // 2
                        harvest_icon_y = img_y - self.ready_harvest_icon.get_height() // 2
                        self.screen.blit(harvest_icon_surface, (harvest_icon_x, harvest_icon_y))
            else:
                lock_x = plot.centerx - self.lock_icon.get_width() // 2
                lock_y = plot.centery - self.lock_icon.get_height() // 2
                glow_surface = pygame.Surface((self.lock_icon.get_width() + 30, self.lock_icon.get_height() + 30), pygame.SRCALPHA)
                glow_radius = int(35 * self.SCALE_X * (1 + 0.2 * math.sin(current_time / 500)))
                pygame.draw.circle(glow_surface, self.GLOW_COLOR, (glow_surface.get_width() // 2, glow_surface.get_height() // 2), glow_radius)
                self.screen.blit(glow_surface, (lock_x - 15, lock_y - 15))
                angle = math.sin(current_time / 1000) * 10
                rotated_lock = pygame.transform.rotate(self.lock_icon, angle)
                lock_rect = rotated_lock.get_rect(center=(plot.centerx, plot.centery))
                self.screen.blit(rotated_lock, lock_rect.topleft)
                if current_time % 200 < self.clock.get_time():
                    self.add_particle(plot.centerx, plot.centery)
                for particle in self.particles:
                    pygame.draw.circle(self.screen, self.PARTICLE_COLOR, (int(particle["x"]), int(particle["y"])), 3)
                    particle["alpha"] = int(255 * (particle["life"] / 1000))
                    particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, (*self.PARTICLE_COLOR[:3], particle["alpha"]), (3, 3), 3)
                    self.screen.blit(particle_surface, (int(particle["x"]) - 3, int(particle["y"]) - 3))

        self.screen.blit(self.back_button_image, (self.back_button.x, self.back_button.y))

        # Draw mana bar
        pygame.draw.rect(self.screen, self.BLACK, (self.MANA_BAR_X - 5, self.MANA_BAR_Y - 5, self.MANA_BAR_WIDTH + 10, self.MANA_BAR_HEIGHT + 10), border_radius=5)
        pygame.draw.rect(self.screen, self.WHITE, (self.MANA_BAR_X, self.MANA_BAR_Y, self.MANA_BAR_WIDTH, self.MANA_BAR_HEIGHT), border_radius=5)
        mana_width = (self.player.get_energy() / self.player.max_energy) * (self.MANA_BAR_WIDTH - 4)
        pygame.draw.rect(self.screen, self.BLUE, (self.MANA_BAR_X + 2, self.MANA_BAR_Y + 2, mana_width, self.MANA_BAR_HEIGHT - 4), border_radius=5)
        energy_text = self.font.render(f"MANA: {self.player.get_energy()}/{self.player.max_energy}", True, self.BLACK)
        self.screen.blit(energy_text, (self.MANA_BAR_X + (self.MANA_BAR_WIDTH - energy_text.get_width()) // 2, self.MANA_BAR_Y + (self.MANA_BAR_HEIGHT - energy_text.get_height()) // 2))

        # Draw time info
        day_text = self.font.render(f"Date: {self.time_system.current_day}", True, self.WHITE)
        time_text = self.font.render(f"Time: {self.time_system.format_time(self.time_system.get_remaining_time())}", True, self.WHITE)
        day_night_text = self.font.render(f"Status: {self.time_system.get_time_of_day()}", True, self.WHITE)
        self.screen.blit(day_text, (self.WIDTH - 150 * self.SCALE_X, 10 * self.SCALE_Y))
        self.screen.blit(time_text, (self.WIDTH - 150 * self.SCALE_X, 30 * self.SCALE_Y))
        self.screen.blit(day_night_text, (self.WIDTH - 150 * self.SCALE_X, 50 * self.SCALE_Y))

        # Draw message if exists
        if self.message and self.message_timer > 0:
            message_surface = self.large_font.render(self.message, True, self.WARNING_COLOR)
            message_rect = message_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
            self.screen.blit(message_surface, message_rect)

        if not self.time_system.is_day():
            night_overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            night_overlay.set_alpha(200)
            night_overlay.fill(self.BLACK)
            self.screen.blit(night_overlay, (0, 0))
            night_message = self.large_font.render("It's night, buddy! You can't be here!", True, self.WHITE)
            self.screen.blit(night_message, night_message.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2)))
        else:
            if self.show_inventory:
                inventory_items, total_pages = self.update_inventory_display()
                pygame.draw.rect(self.screen, self.INVENTORY_BG, (self.inventory_x, self.inventory_y, self.inventory_width, self.inventory_height), border_radius=10)
                for item in inventory_items:
                    pygame.draw.rect(self.screen, self.INVENTORY_CELL_BG, item["rect"], border_radius=5)
                    pygame.draw.rect(self.screen, self.BLACK, item["rect"], 3, border_radius=5)
                    if item["image"]:
                        img_x = item["rect"].x + (self.inventory_cell_size - item["image"].get_width()) // 2
                        img_y = item["rect"].y + (self.inventory_cell_size - item["image"].get_height()) // 2
                        self.screen.blit(item["image"], (img_x, img_y))
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.prev_button, border_radius=5)
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.next_button, border_radius=5)
                prev_text = self.font.render("<", True, self.WHITE)
                next_text = self.font.render(">", True, self.WHITE)
                self.screen.blit(prev_text, (self.prev_button.x + 20 * self.SCALE_X, self.prev_button.y -5 + 2 * self.SCALE_Y))
                self.screen.blit(next_text, (self.next_button.x + 20 * self.SCALE_X, self.next_button.y -5 + 2 * self.SCALE_Y))
                page_text = self.font.render(f"Page {self.current_page + 1}/{total_pages}", True, self.WHITE)
                self.screen.blit(page_text, page_text.get_rect(center=(self.inventory_x + self.inventory_width // 2, self.inventory_y + self.inventory_height-5 - 15 * self.SCALE_Y)))

    def handle_events(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.back_button.collidepoint(mouse_pos):
                    print("Quay lại FarmScene!")
                    running = False  # Thoát khỏi FarmGame để quay lại FarmScene
                if self.time_system.is_day():
                    for index, plot in enumerate(self.plots[:self.player.get_garden_slots()]):
                        if plot.collidepoint(mouse_pos):
                            self.planted_seeds = self.time_system.get_plants()  # Cập nhật planted_seeds trước khi xử lý
                            if self.is_harvesting and index in self.planted_seeds and self.planted_seeds[index]["stage"] == 3:
                                seed_type = self.planted_seeds[index]["seed"]
                                product = self.seed_to_product[seed_type]
                                self.player.inventory.add_item(product, 1)
                                del self.planted_seeds[index]
                                self.time_system.load_plants(self.planted_seeds)
                            elif self.is_watering and index in self.planted_seeds and self.planted_seeds[index]["stage"] < 4:
                                plant = self.planted_seeds[index]
                                if plant["stage"] < 3 and plant["remaining_upgrade_time"] is None:
                                    plant["remaining_upgrade_time"] = self.UPGRADE_TIME
                                    plant["remaining_death_time"] = self.DEATH_TIME
                                    self.watering_animation = True
                                    self.watering_animation_start = pygame.time.get_ticks()
                                    self.time_system.load_plants(self.planted_seeds)
                                    print(f"Watered plant at plot {index} in stage {plant['stage']}!")
                            elif self.is_removing and index in self.planted_seeds:
                                del self.planted_seeds[index]
                                self.time_system.load_plants(self.planted_seeds)
                            elif index not in self.planted_seeds and self.selected_seed is not None:
                                if self.player.get_energy() < self.ENERGY_COST:
                                    self.message = "Not enough mana!"
                                    self.message_timer = self.MESSAGE_DURATION
                                elif not self.player.inventory.has_item(self.selected_seed):
                                    self.message = f"Not enough {self.seed_names[self.selected_seed]}!"
                                    self.message_timer = self.MESSAGE_DURATION
                                else:
                                    energy_success = self.player.reduce_energy(self.ENERGY_COST)
                                    inventory_success = self.player.inventory.remove_item(self.selected_seed, 1)
                                    if energy_success and inventory_success:
                                        self.planted_seeds[index] = {
                                            "seed": self.selected_seed,
                                            "stage": 1,
                                            "remaining_upgrade_time": None,
                                            "remaining_death_time": self.DEATH_TIME,
                                            "center_pos": list(plot.center)
                                        }
                                        self.time_system.load_plants(self.planted_seeds)
                                        print(f"Đã trồng {self.selected_seed} tại ô {index}")
                                        self.selected_seed = None
                    for feature in self.features:
                        if feature["rect"].collidepoint(mouse_pos):
                            if feature["function"] == "plant_menu":
                                self.show_inventory = not self.show_inventory
                                self.is_harvesting = self.is_watering = self.is_removing = False
                            elif feature["function"] == "water":
                                self.is_watering = not self.is_watering
                                self.is_harvesting = self.is_removing = self.show_inventory = False
                            elif feature["function"] == "remove":
                                self.is_removing = not self.is_removing
                                self.is_harvesting = self.is_watering = self.show_inventory = False
                            elif feature["function"] == "harvest":
                                self.is_harvesting = not self.is_harvesting
                                self.is_watering = self.is_removing = self.show_inventory = False
                    if self.show_inventory:
                        inventory_items, total_pages = self.update_inventory_display()
                        for item in inventory_items:
                            if item["rect"].collidepoint(mouse_pos) and item["name"]:
                                self.selected_seed = item["name"]
                                self.show_inventory = False
                        if self.prev_button.collidepoint(mouse_pos) and self.current_page > 0:
                            self.current_page -= 1
                        if self.next_button.collidepoint(mouse_pos) and self.current_page < total_pages - 1:
                            self.current_page += 1
        return running

    def update_cursor(self, current_time):
        mouse_pos = pygame.mouse.get_pos()
        cursor_changed = False
        if self.time_system.is_day():
            if self.is_harvesting:
                pygame.mouse.set_visible(False)
                self.screen.blit(self.sickle_cursor, (mouse_pos[0], mouse_pos[1]))
            elif self.is_watering:
                pygame.mouse.set_visible(False)
                if self.watering_animation and (current_time - self.watering_animation_start < self.WATERING_ANIMATION_DURATION):
                    self.screen.blit(self.watering_can_cursor, (mouse_pos[0], mouse_pos[1]))
                else:
                    self.screen.blit(self.water_can_cursor, (mouse_pos[0], mouse_pos[1]))
                    self.watering_animation = False
            elif self.is_removing:
                pygame.mouse.set_visible(False)
                self.screen.blit(self.sickle_cursor, (mouse_pos[0], mouse_pos[1]))
            else:
                pygame.mouse.set_visible(True)
                for plot in self.plots[:self.player.get_garden_slots()]:
                    if plot.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(self.hover_cursor)
                        cursor_changed = True
                        break
                for feature in self.features:
                    if feature["rect"].collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(self.hover_cursor)
                        cursor_changed = True
                        break
                for plot in self.plots[self.player.get_garden_slots():]:
                    if plot.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(self.hover_cursor)
                        cursor_changed = True
                        break
                if self.back_button.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(self.hover_cursor)
                    cursor_changed = True
                if self.show_inventory:
                    inventory_items, total_pages = self.update_inventory_display()
                    for item in inventory_items:
                        if item["rect"].collidepoint(mouse_pos):
                            pygame.mouse.set_cursor(self.hover_cursor)
                            cursor_changed = True
                            break
                    if self.prev_button.collidepoint(mouse_pos) or self.next_button.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(self.hover_cursor)
                        cursor_changed = True
                if not cursor_changed:
                    pygame.mouse.set_cursor(self.default_cursor)

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_time
            self.last_time = current_time

            self.time_system.update(delta_time)  # Cập nhật thời gian và cây trồng
            self.planted_seeds = self.time_system.get_plants()  # Lấy trạng thái cây trồng mới nhất

            self.update_particles(delta_time)
            self.draw(current_time)
            running = self.handle_events()
            self.update_cursor(current_time)

            if self.message_timer > 0:
                self.message_timer -= delta_time
                if self.message_timer <= 0:
                    self.message = None

            pygame.display.flip()
            self.clock.tick(60)
        
        # Không lưu tự động khi thoát, chỉ trả về trạng thái hiện tại
        return self.player, self.time_system, self.time_system.get_plants()

if __name__ == "__main__":
    game = FarmGame()
    player, time_system, planted_seeds = game.run()
    pygame.quit()