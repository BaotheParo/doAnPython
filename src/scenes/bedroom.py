import pygame
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")

from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Bedroom:
    def __init__(self, game_state, screen, ui):
        self.game_state = game_state
        self.screen = screen
        self.ui = ui
        pygame.display.set_caption("Phòng ngủ")

        self.background_day = pygame.image.load(
            os.path.join(IMAGE_DIR, "backgrounds", "background-phongngu.png")
        ).convert()
        self.background_day = pygame.transform.scale(self.background_day, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.background_night = pygame.image.load(
            os.path.join(IMAGE_DIR, "backgrounds", "background-phongngu-dem.png")
        ).convert()
        self.background_night = pygame.transform.scale(self.background_night, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.bed_rect = pygame.Rect(100, 400, 300, 150)     # Giường
        self.door_rect = pygame.Rect(730, 220, 110, 200)     # Cửa

        self.font = pygame.font.SysFont(None, 24)
        self.tooltip_font = pygame.font.SysFont(None, 22)

        self.running = True
        self.next_scene = None
        self.tooltip = None  # Text tooltip hiển thị

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            self.tooltip = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.ui = self.recreate_ui()
                    self.background_day = pygame.transform.scale(self.background_day, (self.screen.get_width(), self.screen.get_height()))
                    self.background_night = pygame.transform.scale(self.background_night, (self.screen.get_width(), self.screen.get_height()))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    ui_handled = self.ui.handle_event(event)
                    if not ui_handled:
                        action = self.interact(mouse_pos)
                        if action == "farm":
                            from src.scenes.farm import FarmScene
                            print("Chuyển đến FarmScene!")
                            self.running = False
                            self.next_scene = FarmScene(self.game_state, self.screen, self.ui)
                        elif action == "sleep":
                            print("Ngủ hoặc nghỉ ngơi!")
                            self.sleep()

            self.check_tooltip(mouse_pos)
            self.draw(mouse_pos)
            self.ui.draw()
            pygame.display.flip()
            clock.tick(60)

        return self.next_scene

    def sleep(self):
        if self.game_state.time_system.is_day_state:
            # Ban ngày => chuyển sang ban đêm
            self.game_state.time_system.is_day_state = False
            self.game_state.time_system.remaining_day_time = self.game_state.time_system.night_duration
        else:
            # Ban đêm => chuyển sáng => ngày mới
            self.game_state.time_system.is_day_state = True
            self.game_state.time_system.remaining_day_time = self.game_state.time_system.day_duration
            self.game_state.time_system.current_day += 1  # Tăng ngày mới

    def interact(self, pos):
        if self.door_rect.collidepoint(pos):
            return "farm"
        elif self.bed_rect.collidepoint(pos):
            return "sleep"
        return None

    def check_tooltip(self, pos):
        if self.door_rect.collidepoint(pos):
            self.tooltip = "Đi đến farm"
        elif self.bed_rect.collidepoint(pos):
            if self.game_state.time_system.is_day():
                self.tooltip = "Nghỉ ngơi"
            else:
                self.tooltip = "Ngủ"

    def draw(self, mouse_pos):
        if self.game_state.time_system.is_day():
            self.screen.blit(self.background_day, (0, 0))
        else:
            self.screen.blit(self.background_night, (0, 0))

        # Vẽ debug
        time_text = self.font.render(
            f"Ngày: {self.game_state.time_system.current_day} | {self.game_state.time_system.get_time_of_day()}",
            True, (255, 255, 255)
        )
        coord_text = self.font.render(f"Mouse: {mouse_pos}", True, (255, 255, 255))
        self.screen.blit(time_text, (15, 15))
        self.screen.blit(coord_text, (15, 40))

        # Vẽ tooltip nếu có
        if self.tooltip:
            tooltip_surface = self.tooltip_font.render(self.tooltip, True, (255, 255, 255))
            tooltip_bg = pygame.Surface((tooltip_surface.get_width() + 10, tooltip_surface.get_height() + 6))
            tooltip_bg.fill((50, 50, 50))
            tooltip_rect = tooltip_bg.get_rect()
            tooltip_rect.topleft = (mouse_pos[0] + 15, mouse_pos[1] + 15)
            self.screen.blit(tooltip_bg, tooltip_rect)
            self.screen.blit(tooltip_surface, (tooltip_rect.x + 5, tooltip_rect.y + 3))

    def recreate_ui(self):
        from src.core.ui import SettingsUI
        return SettingsUI(self.screen, self.game_state)
