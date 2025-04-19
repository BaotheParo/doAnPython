# src/scenes/menu.py

import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
IMAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "assets", "images"))

from src.core.ui import SettingsUI
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.save_load import SaveLoad

ASSET_PATH = "assets/images"
ICON_PATH = os.path.join(ASSET_PATH, "icons")

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load(os.path.join(ASSET_PATH, "backgrounds", "mainscreen.png")).convert()

        self.play_btn = pygame.image.load(os.path.join(ICON_PATH, "PlayBtn.png")).convert_alpha()
        self.continue_btn = pygame.image.load(os.path.join(ICON_PATH, "ContinueBtn.png")).convert_alpha()
        self.exit_btn = pygame.image.load(os.path.join(ICON_PATH, "icon-quaylai.png")).convert_alpha()

        # Vị trí nút
        self.play_rect = self.play_btn.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.continue_rect = self.continue_btn.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.exit_rect = self.exit_btn.get_rect(center=(SCREEN_WIDTH // 2, 500))

        # Âm thanh
        self.sound_on = pygame.image.load(os.path.join(ICON_PATH, "sound_on.png")).convert_alpha()
        self.sound_off = pygame.image.load(os.path.join(ICON_PATH, "sound_off.png")).convert_alpha()
        self.sound_rect = self.sound_on.get_rect(topleft=(20, 20))
        self.sound_enabled = True

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.play_btn, self.play_rect)
        self.screen.blit(self.continue_btn, self.continue_rect)
        self.screen.blit(self.exit_btn, self.exit_rect)

        # Vẽ biểu tượng âm thanh
        if self.sound_enabled:
            self.screen.blit(self.sound_on, self.sound_rect)
        else:
            self.screen.blit(self.sound_off, self.sound_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.play_rect.collidepoint(pos):
                print("Bắt đầu game mới")  # Thay bằng gọi scene phòng ngủ
                return "new_game"
            elif self.continue_rect.collidepoint(pos):
                print("Hiện danh sách save")  # Thay bằng giao diện chọn file save
                return "load_game"
            elif self.exit_rect.collidepoint(pos):
                pygame.quit()
                sys.exit()
            elif self.sound_rect.collidepoint(pos):
                self.sound_enabled = not self.sound_enabled
        return None
    def update_time_status(self, new_status):
        """Cập nhật trạng thái thời gian (sáng, trưa, chiều, tối)"""
        if new_status in self.icons:
            self.time_status = new_status

