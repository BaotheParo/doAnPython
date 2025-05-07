import pygame
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

from src.core.ui import SettingsUI
from src.actions.fishing_action import start_fishing
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class FishingScene:
    def __init__(self, game_state, screen, ui):
        self.game_state = game_state
        self.screen = screen
        self.ui = ui
        pygame.display.set_caption("Fishing area")

        self.day_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-cauca.png")
        self.night_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds",
                                                  "background-cauca-dem.png")

        self.font = pygame.font.Font(None, 36)

        self.notification_text = "Moved to the fish pond"
        self.notification_surface = self.font.render(self.notification_text, True, (255, 255, 255))
        self.notification_timer = 3000
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

        self.lake_rect = pygame.Rect(515, 450, 485, 200)

        self.hover_color = (200, 200, 200, 10)
        self.hover_surface = pygame.Surface((self.lake_rect.width, self.lake_rect.height), pygame.SRCALPHA)
        self.hover_surface.fill(self.hover_color)

        self.font = pygame.font.SysFont(None, 24)

        self.running = True
        self.ui = SettingsUI(self.screen, self.game_state)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = clock.tick(60)
            self.game_state.time_system.update(delta_time, self.game_state.player)  

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not (self.ui.show_map or self.ui.show_inventory):
                        self.handle_click(mouse_pos)
                    self.ui.handle_event(event)

            if self.game_state.time_system.is_day():
                self.screen.blit(self.day_background, (0, 0))
            else:
                self.screen.blit(self.night_background, (0, 0))

            if self.lake_rect.collidepoint(mouse_pos):
                self.screen.blit(self.hover_surface, (self.lake_rect.x, self.lake_rect.y))

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

            if self.notification_timer > 0:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.notification_start_time
                if elapsed_time < self.notification_timer:
                    text_rect = self.notification_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
                    bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
                    bg_surface.fill((0, 0, 0, 180))
                    self.screen.blit(bg_surface, (text_rect.x - 10, text_rect.y - 5))
                    self.screen.blit(self.notification_surface, text_rect)
                else:
                    self.notification_timer = 0
            self.ui.draw()
            pygame.display.flip()

    def handle_click(self, pos):
        if self.lake_rect.collidepoint(pos):
            print("Start fishing!")
            start_fishing(self.game_state.player, self.screen)  # Chỉ truyền 2 tham số: player và screen
            print("Back to the fishing area!")