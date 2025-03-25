import pygame
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../assets/images"))

from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class SettingsUI:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state  # Sử dụng GameState thay vì player, time_system, planted_seeds riêng
        self.show_menu = False
        self.show_map = False

        self.screen_width, self.screen_height = self.screen.get_size()
        self.menu_width = int(self.screen_width * 0.25)
        self.menu_height = int(self.screen_height * 0.3)
        self.menu_x = (self.screen_width - self.menu_width) // 2
        self.menu_y = (self.screen_height - self.menu_height) // 2

        self.map_width = int(self.screen_width * 0.5)
        self.map_height = int(self.screen_height * 0.5)
        self.map_x = (self.screen_width - self.map_width) // 2
        self.map_y = (self.screen_height - self.map_height) // 2

        self.village_rect_rel = pygame.Rect(100, 150, 80, 80)

        self.icon_settings = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "SettingBtn.png")).convert_alpha()
        self.icon_settings = pygame.transform.scale(self.icon_settings, (50, 50))
        self.icon_settings_rect = self.icon_settings.get_rect(topleft=(self.screen_width - 80, 20))

        self.icon_map = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "mapBtn.png")).convert_alpha()
        self.icon_map = pygame.transform.scale(self.icon_map, (50, 50))
        self.icon_map_rect = self.icon_map.get_rect(topleft=(self.screen_width - 150, 20))

        self.icon_inventory = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-tuido.png")).convert_alpha()
        self.icon_inventory = pygame.transform.scale(self.icon_inventory, (50, 50))
        self.icon_inventory_rect = self.icon_inventory.get_rect(topleft=(self.screen_width - 220, 20))

        self.map_image = pygame.image.load(os.path.join(IMAGE_DIR, "backgrounds", "map.png")).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.map_width, self.map_height))

        self.back_icon = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-quaylai.png")).convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (40, 40))

        self.font = pygame.font.Font(None, int(self.screen_width * 0.02))

        self.button_width = int(self.menu_width * 0.8)
        self.button_height = int(self.menu_height * 0.2)
        self.buttons = [
            {"text": "Save Game", "action": self.save_game_ui, "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
            {"text": "Main Menu", "action": self.main_menu_ui, "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
            {"text": "Exit Game", "action": self.exit_game, "rect": pygame.Rect(0, 0, self.button_width, self.button_height)}
        ]

    def draw(self):
        self.screen.blit(self.icon_settings, self.icon_settings_rect)
        self.screen.blit(self.icon_map, self.icon_map_rect)
        self.screen.blit(self.icon_inventory, self.icon_inventory_rect)

        if self.show_menu:
            pygame.draw.rect(self.screen, (50, 50, 50), (self.menu_x, self.menu_y, self.menu_width, self.menu_height))
            pygame.draw.rect(self.screen, (255, 255, 255), (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 3)
            for i, button in enumerate(self.buttons):
                button_x = self.menu_x + (self.menu_width - self.button_width) // 2
                button_y = self.menu_y + 20 + i * (self.button_height + 10)
                button["rect"].topleft = (button_x, button_y)
                color = (150, 150, 150) if button["rect"].collidepoint(pygame.mouse.get_pos()) else (100, 100, 100)
                pygame.draw.rect(self.screen, color, button["rect"])
                pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2)
                text_surface = self.font.render(button["text"], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button["rect"].center)
                self.screen.blit(text_surface, text_rect)

        if self.show_map:
            border_x = self.map_x - 4
            border_y = self.map_y - 4
            border_w = self.map_width + 8
            border_h = self.map_height + 8
            pygame.draw.rect(self.screen, (155, 173, 183), (border_x, border_y, border_w, border_h), width=4)
            pygame.draw.rect(self.screen, (50, 50, 50), (self.map_x, self.map_y, self.map_width, self.map_height))
            self.screen.blit(self.map_image, (self.map_x, self.map_y))
            self.back_icon_rect = self.back_icon.get_rect(topright=(self.map_x + self.map_width - 10, self.map_y + 10))
            self.screen.blit(self.back_icon, self.back_icon_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.icon_settings_rect.collidepoint(event.pos):
                self.show_menu = not self.show_menu
                self.show_map = False
                return
            if self.icon_map_rect.collidepoint(event.pos):
                self.show_map = not self.show_map
                self.show_menu = False
                return
            if self.show_map and self.back_icon_rect.collidepoint(event.pos):
                self.show_map = False
                return
            if self.show_menu:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()

    def save_game_ui(self):
        self.game_state.save_game()  # Gọi save_game từ GameState
        print("Game đã được lưu từ UI!")
        self.show_menu = False

    def main_menu_ui(self):
        print("Quay về Main Menu...")
        self.show_menu = False

    def exit_game(self):
        print("Thoát game!")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    from src.core.game_state import GameState
    game_state = GameState()
    settings_ui = SettingsUI(screen, game_state)
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                settings_ui = SettingsUI(screen, game_state)
            settings_ui.handle_event(event)

        screen.fill((0, 0, 0))
        settings_ui.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()