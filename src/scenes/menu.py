import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.ui import SettingsUI
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.save_load import SaveLoad
from src.scenes.bedroom import Bedroom

ASSET_PATH = "assets/images"
ICON_PATH = os.path.join(ASSET_PATH, "icons")

class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        # Load background và scale full screen
        self.bg_original = pygame.image.load(os.path.join(ASSET_PATH, "backgrounds", "mainscreen.png")).convert()
        self.bg = pygame.transform.smoothscale(self.bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.play_btn = pygame.image.load(os.path.join(ICON_PATH, "PlayBtn.png")).convert_alpha()
        self.continue_btn = pygame.image.load(os.path.join(ICON_PATH, "ContinueBtn.png")).convert_alpha()
        self.exit_btn = pygame.image.load(os.path.join(ICON_PATH, "icon-quaylai.png")).convert_alpha()

        # Âm thanh
        self.sound_on = pygame.image.load(os.path.join(ICON_PATH, "sound_on.png")).convert_alpha()
        self.sound_off = pygame.image.load(os.path.join(ICON_PATH, "sound_off.png")).convert_alpha()
        self.sound_enabled = True

        # Cập nhật vị trí nút
        self.update_positions()

    def update_positions(self):
        center_x = SCREEN_WIDTH // 2
        base_y = SCREEN_HEIGHT // 2
        spacing = 120

        self.play_rect = self.play_btn.get_rect(center=(center_x, base_y - spacing // 2))
        self.continue_rect = self.continue_btn.get_rect(center=(center_x, base_y + spacing // 2))

        self.sound_rect = self.sound_on.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.exit_rect = self.exit_btn.get_rect(topleft=(20, 20))

    def draw(self):
        self.screen.blit(self.bg, (0, 0))  # Vẽ background đã scale full screen
        self.screen.blit(self.play_btn, self.play_rect)
        self.screen.blit(self.continue_btn, self.continue_rect)

        # Icon
        self.screen.blit(self.exit_btn, self.exit_rect)

        # Sound
        if self.sound_enabled:
            self.screen.blit(self.sound_on, self.sound_rect)
        else:
            self.screen.blit(self.sound_off, self.sound_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.play_rect.collidepoint(pos):
                print("Bắt đầu game mới")  
                return "new_game"
            elif self.continue_rect.collidepoint(pos):
                print("Tiếp tục game")  
                return "load_game"
            elif self.exit_rect.collidepoint(pos):
                pygame.quit()
                sys.exit()
            elif self.sound_rect.collidepoint(pos):
                self.sound_enabled = not self.sound_enabled
        return None

# Test nhanh nếu chạy file riêng
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Main Menu")
    menu = MainMenu(screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            action = menu.handle_event(event)
            if action == "new_game":
                print("Tạo user mới...")  
                from src.core.player import Player
                player = Player()
                SaveLoad.save_game(player)
                bedroom = Bedroom(screen, player)
                bedroom.run()
                running = False

            elif action == "load_game":
                print("Chọn file save...")  
                player = SaveLoad.load_select()
                if player:
                    bedroom = Bedroom(screen, player)
                    bedroom.run()
                running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
