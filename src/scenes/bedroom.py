import pygame
import os
from src.core.time_system import TimeSystem

# Định nghĩa đường dẫn đến ảnh nền
BEDROOM_IMAGE_PATH = os.path.join("assets", "images", "backgrounds", "bedroom.png")

class Bedroom:
    def __init__(self, screen, player, time_system):
        self.screen = screen
        self.player = player
        self.time_system = time_system

        # Load hình ảnh phòng ngủ
        self.background = pygame.image.load(BEDROOM_IMAGE_PATH)

        # Định vị giường và cửa
        self.bed_rect = pygame.Rect(150, 200, 120, 80)  # Vị trí của giường
        self.door_rect = pygame.Rect(500, 200, 80, 120)  # Vị trí của cửa

    def draw(self):
        """Vẽ giao diện phòng ngủ"""
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def interact(self, pos):
        """Xử lý tương tác khi người chơi nhấn chuột"""
        if self.bed_rect.collidepoint(pos):
            self.time_system.toggle_day_night()
            return "sleep"  # Người chơi đã ngủ, ngày mới bắt đầu
        elif self.door_rect.collidepoint(pos):
            return "farm"  # Người chơi đi ra nông trại
        return None
