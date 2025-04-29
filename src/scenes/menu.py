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

ASSET_PATH = "assets/images"
ICON_PATH = os.path.join(ASSET_PATH, "icons")
SAVE_FOLDER = "saves"
os.makedirs(SAVE_FOLDER, exist_ok=True)

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)

        self.bg_original = pygame.image.load(os.path.join(ASSET_PATH, "backgrounds", "mainscreen.png")).convert()
        self.bg = pygame.transform.smoothscale(self.bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.sound_on_img = pygame.image.load(os.path.join(ICON_PATH, "sound_on.png")).convert_alpha()
        self.sound_off_img = pygame.image.load(os.path.join(ICON_PATH, "sound_off.png")).convert_alpha()
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
            color = (255, 255, 0) if hovered else (180, 180, 180)
            font = pygame.font.SysFont(None, 70 if hovered else 60)

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
                return "new_game"
            elif self.buttons["continue"]["rect"].collidepoint(pos):
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
        rect = pygame.Rect((SCREEN_WIDTH - width) // 2, (SCREEN_HEIGHT - height) // 2, width, height)
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
        files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".json")]
        if not files:
            return None

        selected = 0
        button_width = 400
        button_height = 50
        spacing = 20
        max_visible = 6
        scroll_offset = 0

        box_width, box_height = 500, max_visible * (button_height + spacing) + 140
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2

        back_icon = pygame.image.load(os.path.join(ICON_PATH, "icon-quaylai.png")).convert_alpha()
        back_icon = pygame.transform.smoothscale(back_icon, (40, 40))
        back_icon_rect = back_icon.get_rect(topright=(box_x + box_width - 10, box_y + 10))

        clock = pygame.time.Clock()

        while True:
            self.draw()
            pygame.draw.rect(self.screen, (30, 30, 30), (box_x, box_y, box_width, box_height), border_radius=15)
            pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 3, border_radius=15)

            title = font.render("Chọn file lưu để chơi", True, (255, 255, 255))
            title_rect = title.get_rect(center=(box_x + box_width // 2, box_y + 30))
            self.screen.blit(title, title_rect)
            self.screen.blit(back_icon, back_icon_rect)

            buttons = []
            visible_files = files[scroll_offset:scroll_offset + max_visible]

            for i, filename in enumerate(visible_files):
                rect_x = box_x + (box_width - button_width) // 2
                rect_y = box_y + 70 + i * (button_height + spacing)
                rect = pygame.Rect(rect_x, rect_y, button_width, button_height)
                buttons.append((rect, filename))

                is_hovered = rect.collidepoint(pygame.mouse.get_pos())
                is_selected = (scroll_offset + i) == selected
                bg_color = (70, 70, 150) if is_hovered or is_selected else (50, 50, 50)
                border_color = (255, 255, 0) if is_hovered or is_selected else (200, 200, 200)

                pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
                pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=10)

                text = font.render(filename, True, (255, 255, 255))
                text.set_alpha(220)
                text = text.convert_alpha()
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

            # Thanh cuộn
            if len(files) > max_visible:
                scrollbar_height = int((box_height - 140) * max_visible / len(files))
                scrollbar_y = box_y + 70 + int((box_height - 140 - scrollbar_height) * scroll_offset / (len(files) - max_visible))
                pygame.draw.rect(self.screen, (100, 100, 100), (box_x + box_width - 20, box_y + 70, 10, box_height - 140))
                pygame.draw.rect(self.screen, (200, 200, 200), (box_x + box_width - 20, scrollbar_y, 10, scrollbar_height))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click
                        if back_icon_rect.collidepoint(event.pos):
                            return None
                        for i, (rect, filename) in enumerate(buttons):
                            if rect.collidepoint(event.pos):
                                return os.path.join(SAVE_FOLDER, filename)

                    elif event.button == 4:  # Cuộn lên
                        if scroll_offset > 0:
                            scroll_offset -= 1
                            selected = max(selected - 1, 0)

                    elif event.button == 5:  # Cuộn xuống
                        if scroll_offset + max_visible < len(files):
                            scroll_offset += 1
                            selected = min(selected + 1, len(files) - 1)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(files)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(files)
                    elif event.key == pygame.K_RETURN:
                        return os.path.join(SAVE_FOLDER, files[selected])
                    elif event.key == pygame.K_ESCAPE:
                        return None

                    # Điều chỉnh scroll_offset theo selection
                    if selected < scroll_offset:
                        scroll_offset = selected
                    elif selected >= scroll_offset + max_visible:
                        scroll_offset = selected - max_visible + 1

            clock.tick(60)






def show_message(screen, text, duration=2):
    font = pygame.font.SysFont(None, 50)
    rect = pygame.Rect((SCREEN_WIDTH - 400) // 2, (SCREEN_HEIGHT - 100) // 2, 400, 100)
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < duration * 1000:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (50, 50, 50), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 3)

        text_surface = font.render(text, True, (255, 255, 0))
        text_surface.set_alpha(220)
        text_surface = text_surface.convert_alpha()
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

        pygame.display.update()
        pygame.time.delay(10)

# --- Main ---
if __name__ == "__main__":
    from src.core.time_system import TimeSystem

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")
    menu = MainMenu(screen)
    clock = pygame.time.Clock()

    running = True
    next_scene = None

    while running:
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            action = menu.handle_event(event)
            if action == "new_game":
                if not SaveLoad.is_empty_save():
                    if not menu.confirm_new_game():
                        continue
                    SaveLoad.backup_save()

                files = [f for f in os.listdir(SAVE_FOLDER) if f.startswith("save_data_") and f.endswith(".json")]
                existing_nums = []
                for f in files:
                    try:
                        num = int(f[len("save_data_"):-len(".json")])
                        existing_nums.append(num)
                    except ValueError:
                        pass
                n = 1
                while n in existing_nums:
                    n += 1

                save_filename = f"save_data_{n}.json"
                new_save_path = os.path.join(SAVE_FOLDER, save_filename)

                player = Player()
                player.time_system = TimeSystem()

                with open(new_save_path, 'w') as f:
                    json.dump(player.to_dict(), f)

                SaveLoad.current_save_file = save_filename
                SaveLoad.save_game(player)

                ui = SettingsUI(screen, player)
                bedroom = Bedroom(player, screen, ui)
                next_scene = bedroom.run()
                running = False

            elif action == "load_game":
                files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".json")]
                if not files:
                    show_message(screen, "Không tìm thấy file lưu!", 2)
                    continue

                filepath = menu.choose_save_file()
                if filepath:
                    filename = os.path.basename(filepath)
                    player = SaveLoad.load_game(filename)
                    if player:
                        SaveLoad.current_save_file = filename
                        player.time_system = TimeSystem()
                        ui = SettingsUI(screen, player)
                        bedroom = Bedroom(player, screen, ui)
                        next_scene = bedroom.run()
                        running = False


        pygame.display.update()
        clock.tick(60)

    while next_scene:
        next_scene = next_scene.run()

    pygame.quit()
