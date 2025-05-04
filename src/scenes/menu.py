import pygame
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.ui import SettingsUI
from src.core.player import Player
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.save_load import SaveLoad
from src.scenes.bedroom import Bedroom

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
ASSET_PATH = os.path.join(BASE_DIR, "assets", "images")
ICON_PATH = os.path.join(ASSET_PATH, "icons")
SAVE_FOLDER = os.path.join(BASE_DIR, "saves")
os.makedirs(SAVE_FOLDER, exist_ok=True)

class MainMenu:
    def __init__(self, screen, game_state, ui):
        self.screen = screen
        self.game_state = game_state
        self.ui = ui
        self.font = pygame.font.SysFont(None, 60)

        try:
            self.bg_original = pygame.image.load(os.path.join(ASSET_PATH, "backgrounds", "mainscreen.png")).convert()
        except FileNotFoundError:
            print(f"Error: File 'mainscreen.png' not found in {os.path.join(ASSET_PATH, 'backgrounds')}")
            self.bg_original = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_original.fill((0, 0, 0))
        self.bg = pygame.transform.smoothscale(self.bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

        try:
            self.sound_on_img = pygame.image.load(os.path.join(ICON_PATH, "sound_on.png")).convert_alpha()
            self.sound_off_img = pygame.image.load(os.path.join(ICON_PATH, "sound_off.png")).convert_alpha()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.sound_on_img = pygame.Surface((40, 40), pygame.SRCALPHA)
            self.sound_off_img = pygame.Surface((40, 40), pygame.SRCALPHA)
            self.sound_on_img.fill((255, 255, 255, 128))
            self.sound_off_img.fill((255, 0, 0, 128))
        self.scale_sound_icons(40)
        self.sound_enabled = True
        self.sound_rect = self.sound_on_img.get_rect(topright=(SCREEN_WIDTH - 20, 20))

        self.buttons = {}
        self.create_buttons()

    def scale_sound_icons(self, base_width):
        ratio = base_width / self.sound_on_img.get_width()
        ratio *= 1.5
        new_size = (int(self.sound_on_img.get_width() * ratio), int(self.sound_on_img.get_height() * ratio))
        self.sound_on_img = pygame.transform.smoothscale(self.sound_on_img, new_size)
        self.sound_off_img = pygame.transform.smoothscale(self.sound_off_img, new_size)

    def create_buttons(self):
        labels = ["Start", "Exit"]
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 100
        spacing = 120
        button_width = 300
        button_height = 60

        for i, label in enumerate(labels):
            rect = pygame.Rect(center_x - button_width // 2, start_y + i * spacing, button_width, button_height)
            self.buttons[label.lower()] = {
                "label": label,
                "rect": rect
            }

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for key, button in self.buttons.items():
            hovered = button["rect"].collidepoint(mouse_pos)
            color = (255, 255, 0) if hovered else (180, 180, 180)
            font = pygame.font.SysFont(None, 70 if hovered else 60)

            pygame.draw.rect(self.screen, (50, 50, 50), button["rect"])
            pygame.draw.rect(self.screen, color, button["rect"], 3)

            text_surface = font.render(button["label"], True, color)
            text_surface.set_alpha(180)
            text_surface = text_surface.convert_alpha()
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

        if self.sound_enabled:
            self.screen.blit(self.sound_on_img, self.sound_rect)
        else:
            self.screen.blit(self.sound_off_img, self.sound_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.buttons["start"]["rect"].collidepoint(pos):
                return "start"
            elif self.buttons["exit"]["rect"].collidepoint(pos):
                return "exit"
            elif self.sound_rect.collidepoint(pos):
                self.sound_enabled = not self.sound_enabled
        return None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        next_scene = None

        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    next_scene = None
                    break

                action = self.handle_event(event)
                if action == "start":
                    # Tải dữ liệu save hiện tại nếu có, hoặc tạo player mới nếu không có
                    if SaveLoad.current_save_file:
                        player = SaveLoad.load_game(SaveLoad.current_save_file)
                        if player:
                            player.time_system = self.game_state.time_system
                            self.game_state.player = player
                    else:
                        player = Player()
                        player.time_system = self.game_state.time_system
                        self.game_state.player = player
                    next_scene = Bedroom(self.game_state, self.screen, self.ui)
                    running = False
                elif action == "exit":
                    running = False
                    next_scene = None
                    break

            pygame.display.update()
            clock.tick(60)

        return next_scene

    def show_message(self, text, duration=2):
        font = pygame.font.SysFont(None, 50)
        rect = pygame.Rect((SCREEN_WIDTH - 400) // 2, (SCREEN_HEIGHT - 100) // 2, 400, 100)
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < duration * 1000:
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (50, 50, 50), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)

            text_surface = font.render(text, True, (255, 255, 0))
            text_surface.set_alpha(220)
            text_surface = text_surface.convert_alpha()
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

            pygame.display.update()
            pygame.time.delay(10)