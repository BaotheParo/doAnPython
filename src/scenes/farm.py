import pygame
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

from src.core.ui import SettingsUI
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.actions.planting import FarmGame

class FarmScene:
    def __init__(self, game_state, screen, ui):
        self.game_state = game_state
        self.screen = screen
        self.ui = SettingsUI(self.screen, self.game_state)
        pygame.display.set_caption("Khu vực nông trại")

        self.day_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "bangground-nongtrai.png")
        self.night_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-nongtrai-dem.png")
        self.font = pygame.font.Font(None, 36)

        # Thông báo khi vào làng
        self.notification_text = "Đã di chuyển tới Nông trại"
        self.notification_surface = self.font.render(self.notification_text, True, (255, 255, 255))
        self.notification_timer = 3000  # Hiển thị trong 3 giây (3000ms)
        self.notification_start_time = pygame.time.get_ticks()


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

        self.font = pygame.font.SysFont(None, 24)
        self.message_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.tooltip_font = pygame.font.SysFont("Arial", 20, bold=True)  # Font cho tooltip

        self.show_night_message = False
        self.night_message_timer = 0
        self.night_message_duration = 3000

        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = clock.tick(60)
            self.game_state.time_system.update(delta_time)

            mouse_pos = pygame.mouse.get_pos()
            # Thay đổi con trỏ chuột khi hover
            if self.farm_plot_rect.collidepoint(mouse_pos) or self.bedroom_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    continue
                ui_handled = self.ui.handle_event(event)
                if ui_handled:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(mouse_pos)

            if self.game_state.time_system.is_day():
                self.screen.blit(self.day_background, (0, 0))
            else:
                self.screen.blit(self.night_background, (0, 0))

            # Hiển thị tooltip
            if self.farm_plot_rect.collidepoint(mouse_pos):
                self.render_tooltip("Farm", mouse_pos)
            elif self.bedroom_rect.collidepoint(mouse_pos):
                self.render_tooltip("Bedroom", mouse_pos)

            coord_text = self.font.render(f"Mouse: {mouse_pos}", True, WHITE)
            coord_bg = pygame.Surface((150, 25))
            coord_bg.fill((50, 50, 50))
            self.screen.blit(coord_bg, (10, 10))
            self.screen.blit(coord_text, (15, 15))

            time_text = self.font.render(
                f"Day: {self.game_state.time_system.current_day} | {self.game_state.time_system.get_time_of_day()} | Time Left: {self.game_state.time_system.format_time(self.game_state.time_system.get_remaining_time())}",
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

            if self.notification_timer > 0:
                    current_time = pygame.time.get_ticks()
                    elapsed_time = current_time - self.notification_start_time
                    if elapsed_time < self.notification_timer:
                        # Tính toán vị trí giữa màn hình
                        text_rect = self.notification_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
                        # Vẽ nền tối mờ cho thông báo
                        bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
                        bg_surface.fill((0, 0, 0, 180))  # Nền đen mờ
                        self.screen.blit(bg_surface, (text_rect.x - 10, text_rect.y - 5))
                        # Vẽ văn bản
                        self.screen.blit(self.notification_surface, text_rect)
                    else:
                        self.notification_timer = 0  # Tắt thông báo sau khi hết thời gian
            self.ui.draw()
            pygame.display.flip()

    def handle_click(self, pos):
        if self.farm_plot_rect.collidepoint(pos):
            if not self.game_state.time_system.is_day():
                self.show_night_message = True
                self.night_message_timer = self.night_message_duration
            else:
                print("Chuyển đến khu vực trồng trọt!")
                farm_game = FarmGame(self.game_state.player, self.game_state.time_system, self.game_state.planted_seeds)
                self.game_state.player, self.game_state.time_system, self.game_state.planted_seeds = farm_game.run()
                self.game_state.time_system.load_plants(self.game_state.planted_seeds)
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.display.set_caption("Khu vực nông trại")
                self.ui = SettingsUI(self.screen, self.game_state)
                print(f"Updated SettingsUI with planted_seeds: {self.game_state.planted_seeds}")
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

    def render_tooltip(self, text, mouse_pos):
        """Hiển thị tooltip với văn bản và vị trí chuột"""
        text_surface = self.tooltip_font.render(text, True, WHITE)
        padding = 5
        bg_width = text_surface.get_width() + padding * 2
        bg_height = text_surface.get_height() + padding * 2
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (50, 50, 50, 200), (0, 0, bg_width, bg_height), border_radius=5)
        
        # Đặt vị trí tooltip gần chuột, lệch xuống dưới và sang phải
        tooltip_x = mouse_pos[0] + 10
        tooltip_y = mouse_pos[1] + 10
        # Đảm bảo tooltip không vượt ra ngoài màn hình
        if tooltip_x + bg_width > SCREEN_WIDTH:
            tooltip_x = SCREEN_WIDTH - bg_width
        if tooltip_y + bg_height > SCREEN_HEIGHT:
            tooltip_y = SCREEN_HEIGHT - bg_height

        self.screen.blit(bg_surface, (tooltip_x, tooltip_y))
        self.screen.blit(text_surface, (tooltip_x + padding, tooltip_y + padding))