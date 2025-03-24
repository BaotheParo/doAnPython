import pygame
import os, sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

from src.core.player import Player
from src.core.ui import SettingsUI
from src.core.time_system import TimeSystem
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.actions.planting import FarmGame

class FarmScene:
    def __init__(self, player, screen, ui):
        self.player = player
        self.screen = screen
        self.ui = ui
        self.FARM_DATA_FILE = os.path.join(BASE_DIR, "src", "core", "farm_data.json")
        self.time_system = TimeSystem()  # Khởi tạo TimeSystem
        self.time_system.load_time_data()  # Load dữ liệu thời gian
        self.planted_seeds = self.load_farm_data()  # Load dữ liệu cây trồng
        self.time_system.load_plants(self.planted_seeds)  # Truyền planted_seeds vào TimeSystem
        pygame.display.set_caption("Khu vực nông trại")

        self.day_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "bangground-nongtrai.png")
        self.night_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-nongtrai-dem.png")

        try:
            self.day_background = pygame.image.load(self.day_background_path).convert()
            self.day_background = pygame.transform.scale(self.day_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_background = pygame.image.load(self.night_background_path).convert()
            self.night_background = pygame.transform.scale(self.night_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file - {e}")
            self.day_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.day_background.fill((100, 200, 100))
            self.night_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_background.fill((0, 0, 50))

        self.farm_plot_rect = pygame.Rect(3, 358, 300, 200)
        self.bedroom_rect = pygame.Rect(582, 286, 300, 200)

        self.hover_color = (200, 200, 200, 100)
        self.hover_surface = pygame.Surface((self.farm_plot_rect.width, self.farm_plot_rect.height), pygame.SRCALPHA)
        self.hover_surface.fill(self.hover_color)
        self.new_area_hover_surface = pygame.Surface((self.bedroom_rect.width, self.bedroom_rect.height), pygame.SRCALPHA)
        self.new_area_hover_surface.fill(self.hover_color)

        self.font = pygame.font.SysFont(None, 24)
        self.message_font = pygame.font.SysFont("Arial", 48, bold=True)

        self.show_night_message = False
        self.night_message_timer = 0
        self.night_message_duration = 3000

        self.running = True

    def load_farm_data(self):
        try:
            with open(self.FARM_DATA_FILE, "r") as f:
                farm_data = json.load(f)
                return {int(index): {
                    "seed": plant["seed"],
                    "stage": plant["stage"],
                    "remaining_upgrade_time": plant["remaining_upgrade_time"],
                    "remaining_death_time": plant["remaining_death_time"],
                    "center_pos": tuple(plant["center_pos"])
                } for index, plant in farm_data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = clock.tick(60)
            self.time_system.update(delta_time)  # Cập nhật thời gian và cây trồng
            self.planted_seeds = self.time_system.get_plants()  # Lấy trạng thái cây trồng mới nhất

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(mouse_pos)
                    self.ui.handle_event(event)

            if self.time_system.is_day():
                self.screen.blit(self.day_background, (0, 0))
            else:
                self.screen.blit(self.night_background, (0, 0))

            if self.farm_plot_rect.collidepoint(mouse_pos):
                self.screen.blit(self.hover_surface, (self.farm_plot_rect.x, self.farm_plot_rect.y))
            if self.bedroom_rect.collidepoint(mouse_pos):
                self.screen.blit(self.new_area_hover_surface, (self.bedroom_rect.x, self.bedroom_rect.y))

            coord_text = self.font.render(f"Mouse: {mouse_pos}", True, WHITE)
            coord_bg = pygame.Surface((150, 25))
            coord_bg.fill((50, 50, 50))
            self.screen.blit(coord_bg, (10, 10))
            self.screen.blit(coord_text, (15, 15))

            time_text = self.font.render(
                f"Day: {self.time_system.current_day} | {self.time_system.get_time_of_day()} | Time Left: {self.time_system.format_time(self.time_system.get_remaining_time())}",
                True, WHITE
            )
            time_bg = pygame.Surface((300, 25))
            time_bg.fill((50, 50, 50))
            self.screen.blit(time_bg, (10, 40))
            self.screen.blit(time_text, (15, 45))

            if self.show_night_message:
                self.render_night_message()
                self.night_message_timer -= delta_time
                if self.night_message_timer <= 0:
                    self.show_night_message = False

            self.ui.draw()
            pygame.display.flip()

        # Không lưu tự động khi thoát
        pygame.quit()

    def handle_click(self, pos):
        if self.farm_plot_rect.collidepoint(pos):
            if not self.time_system.is_day():
                self.show_night_message = True
                self.night_message_timer = self.night_message_duration
            else:
                print("Chuyển đến khu vực trồng trọt!")
                farm_game = FarmGame(self.player, self.time_system, self.planted_seeds)
                self.player, self.time_system, self.planted_seeds = farm_game.run()
                self.time_system.load_plants(self.planted_seeds)  # Cập nhật lại planted_seeds vào TimeSystem
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.display.set_caption("Khu vực nông trại")
                self.ui = SettingsUI(self.screen, self.player, self.time_system, self.planted_seeds)
                print(f"Updated SettingsUI with planted_seeds: {self.planted_seeds}")
        elif self.bedroom_rect.collidepoint(pos):
            print("Chuyển đến giường ngủ")

    def render_night_message(self):
        message_text = "The moon whispers: 'Rest now, the farm sleeps under starry skies!'"
        text_surface = self.message_font.render(message_text, True, (255, 255, 200))
        padding = 17
        bg_width = text_surface.get_width() + padding * 2
        bg_height = text_surface.get_height() + padding * 2
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (20, 20, 50, 180), (0, 0, bg_width, bg_height), border_radius=15)
        pygame.draw.rect(bg_surface, (100, 100, 200, 100), (5, 5, bg_width - 10, bg_height - 10), 5, border_radius=15)
        bg_x = (SCREEN_WIDTH - bg_width) // 2
        bg_y = (SCREEN_HEIGHT - bg_height) // 2
        text_x = bg_x + padding
        text_y = bg_y + padding
        self.screen.blit(bg_surface, (bg_x, bg_y))
        self.screen.blit(text_surface, (text_x, text_y))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player()
    time_system = TimeSystem()
    time_system.load_time_data()
    settings_ui = SettingsUI(screen, player, time_system)
    farm_scene = FarmScene(player, screen, settings_ui)
    farm_scene.run()