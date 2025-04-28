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

SAVE_FOLDER = "saves"
os.makedirs(SAVE_FOLDER, exist_ok=True)

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)

        # Không cần khởi tạo self.save_load

        # Background
        self.bg_original = pygame.image.load(os.path.join(ASSET_PATH, "backgrounds", "mainscreen.png")).convert()
        self.bg = pygame.transform.smoothscale(self.bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Icon Sound
        self.sound_on_img = pygame.image.load(os.path.join(ICON_PATH, "sound_on.png")).convert_alpha()
        self.sound_off_img = pygame.image.load(os.path.join(ICON_PATH, "sound_off.png")).convert_alpha()
        self.scale_sound_icons(40)
        self.sound_enabled = True
        self.sound_rect = self.sound_on_img.get_rect(topright=(SCREEN_WIDTH - 20, 20))

        # Buttons
        self.buttons = {}
        self.create_buttons()

    def scale_sound_icons(self, base_width):
        ratio = base_width / self.sound_on_img.get_width()
        ratio *= 1.5
        new_size = (int(self.sound_on_img.get_width() * ratio), int(self.sound_on_img.get_height() * ratio))
        self.sound_on_img = pygame.transform.smoothscale(self.sound_on_img, new_size)
        self.sound_off_img = pygame.transform.smoothscale(self.sound_off_img, new_size)

    def create_buttons(self):
        labels = ["Start", "Continue", "Exit"]
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 100
        spacing = 80

        for i, label in enumerate(labels):
            text_surface = self.font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(center_x, start_y + i * spacing))
            self.buttons[label.lower()] = {
                "label": label,
                "rect": text_rect
            }

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for key, button in self.buttons.items():
            hovered = button["rect"].collidepoint(mouse_pos)
            if hovered:
                color = (255, 255, 0)
                font = pygame.font.SysFont(None, 70)
            else:
                color = (180, 180, 180)
                font = pygame.font.SysFont(None, 60)

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
                if not SaveLoad.is_empty_save():
                    if not self.confirm_new_game():
                        return None
                    else:
                        SaveLoad.backup_save()  # backup theo số tự động
                SaveLoad.reset_save()
                return "new_game"

            elif self.buttons["continue"]["rect"].collidepoint(pos):
                save_file = self.choose_save_file()
                if save_file:
                    SaveLoad.load_file(save_file)
                    return "load_game"

            elif self.buttons["exit"]["rect"].collidepoint(pos):
                pygame.quit()
                sys.exit()
            elif self.sound_rect.collidepoint(pos):
                self.sound_enabled = not self.sound_enabled
        return None

    def confirm_new_game(self):
        font = pygame.font.SysFont(None, 40)
        width, height = 500, 200
        rect = pygame.Rect((SCREEN_WIDTH - width)//2, (SCREEN_HEIGHT - height)//2, width, height)
        while True:
            self.draw()
            pygame.draw.rect(self.screen, (50, 50, 50), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)

            text = font.render("Bạn có chắc chắn muốn chơi mới?", True, (255, 255, 255))
            text.set_alpha(180)
            text = text.convert_alpha()
            self.screen.blit(text, (rect.x + 20, rect.y + 40))

            yes_btn = pygame.Rect(rect.x + 50, rect.y + 120, 150, 50)
            no_btn = pygame.Rect(rect.x + 300, rect.y + 120, 150, 50)

            self.draw_simple_button(yes_btn, "Có")
            self.draw_simple_button(no_btn, "Không")

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if yes_btn.collidepoint(pos):
                        return True
                    if no_btn.collidepoint(pos):
                        return False

    def draw_simple_button(self, rect, text):
        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(text, True, (255, 255, 255))
        text_surface.set_alpha(180)
        text_surface = text_surface.convert_alpha()
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def choose_save_file(self):
        font = pygame.font.SysFont(None, 40)
        files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".dat")]
        if not files:
            return None

        selected = 0
        while True:
            self.draw()
            y = 100
            for i, filename in enumerate(files):
                color = (255, 255, 0) if i == selected else (255, 255, 255)
                text = font.render(filename, True, color)
                text.set_alpha(180)
                text = text.convert_alpha()
                self.screen.blit(text, (SCREEN_WIDTH//2 - 200, y))
                y += 60

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(files)
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(files)
                    if event.key == pygame.K_RETURN:
                        return os.path.join(SAVE_FOLDER, files[selected])


# Test nhanh
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
                from src.core.player import Player
                if not SaveLoad.is_empty_save():
                    if menu.confirm_new_game():
                        SaveLoad.backup_save()
                        player = Player()
                        SaveLoad.save_game(player)
                        bedroom = Bedroom(screen, player)
                        bedroom.run()
                        running = False
                else:
                    player = Player()
                    SaveLoad.save_game(player)
                    bedroom = Bedroom(screen, player)
                    bedroom.run()
                    running = False

            elif action == "load_game":
                filepath = menu.choose_save_file()
                if filepath:
                    player = SaveLoad.load_file(filepath)
                    if player:
                        bedroom = Bedroom(screen, player)
                        bedroom.run()
                        running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
