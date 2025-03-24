import pygame
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

from src.core.player import Player
from src.core.ui import SettingsUI
from src.core.time_system import TimeSystem
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class FarmScene:
    def __init__(self, player, time_system, screen, ui):
        self.player = player
        self.time_system = time_system
        self.ui = ui
        self.screen = screen
        pygame.display.set_caption("Khu vực nông trại")

        # Đường dẫn đến các file background
        self.day_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "bangground-nongtrai.png")
        self.night_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-nongtrai-dem.png")

        try:
            # Tải và scale background ban ngày
            self.day_background = pygame.image.load(self.day_background_path).convert()
            self.day_background = pygame.transform.scale(self.day_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

            # Tải và scale background ban đêm
            self.night_background = pygame.image.load(self.night_background_path).convert()
            self.night_background = pygame.transform.scale(self.night_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file - {e}")
            self.day_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.day_background.fill((100, 200, 100))  # Màu xanh lá mặc định cho ban ngày
            self.night_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_background.fill((0, 0, 50))  # Màu xanh đậm mặc định cho ban đêm

        # Tạo khu vực trồng trọt (farm plot)
        self.farm_plot_rect = pygame.Rect(3, 358, 300, 200)  # (x, y, width, height)

        # Tạo khu vực mới tại vị trí (582, 286)
        self.bedroom_rect = pygame.Rect(582, 286, 300, 200)  # (x, y, width, height)

        # Hiệu ứng hover khi chuột di qua khu vực trồng trọt và khu vực mới
        self.hover_color = (200, 200, 200, 10)  # Màu xám nhạt, trong suốt
        self.hover_surface = pygame.Surface((self.farm_plot_rect.width, self.farm_plot_rect.height), pygame.SRCALPHA)
        self.hover_surface.fill(self.hover_color)
        # Hiệu ứng hover cho khu vực mới (cùng kích thước với farm_plot_rect)
        self.new_area_hover_surface = pygame.Surface((self.bedroom_rect.width, self.bedroom_rect.height), pygame.SRCALPHA)
        self.new_area_hover_surface.fill(self.hover_color)

        # Font để hiển thị tọa độ chuột và thời gian
        self.font = pygame.font.SysFont(None, 24)

        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = clock.tick(60)  # Thời gian trôi qua giữa các khung hình (ms)
            self.time_system.update(delta_time)  # Cập nhật thời gian trong game

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.time_system.save_time_data()  # Lưu thời gian trước khi thoát
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(mouse_pos)
                    self.ui.handle_event(event)

            # Vẽ background dựa trên thời gian
            if self.time_system.is_day():
                self.screen.blit(self.day_background, (0, 0))
            else:
                self.screen.blit(self.night_background, (0, 0))

            # Vẽ hiệu ứng hover khi chuột di qua khu vực trồng trọt
            if self.farm_plot_rect.collidepoint(mouse_pos):
                self.screen.blit(self.hover_surface, (self.farm_plot_rect.x, self.farm_plot_rect.y))

            # Vẽ hiệu ứng hover khi chuột di qua khu vực mới
            if self.bedroom_rect.collidepoint(mouse_pos):
                self.screen.blit(self.new_area_hover_surface, (self.bedroom_rect.x, self.bedroom_rect.y))

            # Hiển thị tọa độ chuột trên màn hình
            coord_text = self.font.render(f"Mouse: {mouse_pos}", True, WHITE)
            coord_bg = pygame.Surface((150, 25))
            coord_bg.fill((50, 50, 50))
            self.screen.blit(coord_bg, (10, 10))
            self.screen.blit(coord_text, (15, 15))

            # Hiển thị thời gian hiện tại (ngày/đêm và thời gian còn lại)
            time_text = self.font.render(
                f"Day: {self.time_system.current_day} | {self.time_system.get_time_of_day()} | Time Left: {self.time_system.format_time(self.time_system.get_remaining_time())}",
                True, WHITE
            )
            time_bg = pygame.Surface((300, 25))
            time_bg.fill((50, 50, 50))
            self.screen.blit(time_bg, (10, 40))
            self.screen.blit(time_text, (15, 45))

            self.ui.draw()

            pygame.display.flip()

    def handle_click(self, pos):
        if self.farm_plot_rect.collidepoint(pos):
            print("Chuyển đến khu vực trồng trọt!")
            print("Quay lại khu vực nông trại!")
        elif self.bedroom_rect.collidepoint(pos):
            print("Chuyển đến giường ngủ")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    from src.core.player import Player
    from src.core.time_system import TimeSystem
    from src.core.ui import SettingsUI

    player = Player()
    settings_ui = SettingsUI(screen, player)
    time_system = TimeSystem()
    farm_scene = FarmScene(player, time_system, screen, settings_ui)
    farm_scene.run()
    pygame.quit()