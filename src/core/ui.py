import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../assets/images"))

class SettingsUI:
    def __init__(self, screen):
        self.screen = screen
        self.show_menu = False   # Trạng thái menu
        self.show_map = False    # Trạng thái bản đồ

        # Lấy kích thước màn hình
        self.screen_width, self.screen_height = self.screen.get_size()

        # Menu
        self.menu_width = int(self.screen_width * 0.25)
        self.menu_height = int(self.screen_height * 0.3)
        self.menu_x = (self.screen_width - self.menu_width) // 2
        self.menu_y = (self.screen_height - self.menu_height) // 2

        # Map chiếm 50% màn hình
        self.map_width = int(self.screen_width * 0.5)
        self.map_height = int(self.screen_height * 0.5)
        self.map_x = (self.screen_width - self.map_width) // 2
        self.map_y = (self.screen_height - self.map_height) // 2

        # Icons
        self.icon_settings = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "SettingBtn.png")).convert_alpha()
        self.icon_settings = pygame.transform.scale(self.icon_settings, (50, 50))
        self.icon_settings_rect = self.icon_settings.get_rect(topleft=(self.screen_width - 80, 20))

        self.icon_map = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "mapBtn.png")).convert_alpha()
        self.icon_map = pygame.transform.scale(self.icon_map, (50, 50))
        self.icon_map_rect = self.icon_map.get_rect(topleft=(self.screen_width - 150, 20))

        self.icon_inventory = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-tuido.png")).convert_alpha()
        self.icon_inventory = pygame.transform.scale(self.icon_inventory, (50, 50))
        self.icon_inventory_rect = self.icon_inventory.get_rect(topleft=(self.screen_width - 220, 20))

        # Ảnh bản đồ
        self.map_image = pygame.image.load(os.path.join(IMAGE_DIR, "backgrounds", "map.png")).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.map_width, self.map_height))

        # Nút "Quay lại"
        self.back_icon = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-quaylai.png")).convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (40, 40))

        # Font
        self.font = pygame.font.Font(None, int(self.screen_width * 0.02))

        # Danh sách button menu
        self.button_width = int(self.menu_width * 0.8)
        self.button_height = int(self.menu_height * 0.2)
        self.buttons = [
            {"text": "Save Game", "action": self.save_game, 
             "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
            {"text": "Main Menu", "action": self.main_menu, 
             "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
            {"text": "Exit Game", "action": self.exit_game, 
             "rect": pygame.Rect(0, 0, self.button_width, self.button_height)}
        ]

    def draw(self):
        # Vẽ icon settings, map, inventory
        self.screen.blit(self.icon_settings, self.icon_settings_rect)
        self.screen.blit(self.icon_map, self.icon_map_rect)
        self.screen.blit(self.icon_inventory, self.icon_inventory_rect)

        # Vẽ menu settings nếu đang mở
        if self.show_menu:
            pygame.draw.rect(self.screen, (50, 50, 50), 
                             (self.menu_x, self.menu_y, self.menu_width, self.menu_height))
            pygame.draw.rect(self.screen, (255, 255, 255), 
                             (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 
                             width=3)  # Tăng width viền cho nổi

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

        # Vẽ map nếu đang mở
        if self.show_map:
            border_x = self.map_x - 4
            border_y = self.map_y - 4
            border_w = self.map_width + 8
            border_h = self.map_height + 8
            # Nền xám khung map
            pygame.draw.rect(self.screen, (155, 173, 183),
                 (border_x, border_y, border_w, border_h),
                 width=4)

# Vẽ nền bên trong (tuỳ ý) hoặc để trống
            pygame.draw.rect(self.screen, (50, 50, 50),
                 (self.map_x, self.map_y, self.map_width, self.map_height))

            # Vẽ ảnh map lên khung
            self.screen.blit(self.map_image, (self.map_x, self.map_y))

            # Tính vị trí nút "Quay lại" ở góc trên phải khung map
            self.back_icon_rect = self.back_icon.get_rect(
                topright=(self.map_x + self.map_width - 10, self.map_y + 10)
            )
            self.screen.blit(self.back_icon, self.back_icon_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Nếu bấm icon settings -> mở/tắt menu
            if self.icon_settings_rect.collidepoint(event.pos):
                self.show_menu = not self.show_menu
                self.show_map = False
                return

            # Nếu bấm icon map -> mở map
            if self.icon_map_rect.collidepoint(event.pos):
                self.show_map = not self.show_map
                self.show_menu = False
                return

            # Nếu map đang mở, kiểm tra click nút back
            if self.show_map:
                if self.back_icon_rect.collidepoint(event.pos):
                    self.show_map = False
                    return

            # Nếu menu đang mở, kiểm tra click các nút menu
            if self.show_menu:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()

    def save_game(self):
        print("Lưu game...")
        self.show_menu = False

    def main_menu(self):
        print("Quay về Main Menu...")
        self.show_menu = False

    def exit_game(self):
        print("Thoát game!")
        pygame.quit()
        exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Test UI Settings")

    # Load ảnh background
    background = pygame.image.load(os.path.join(IMAGE_DIR, "backgrounds", "mainscreen.png")).convert()
    background = pygame.transform.scale(background, (1280, 720))

    settings_ui = SettingsUI(screen)
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                settings_ui = SettingsUI(screen)

            settings_ui.handle_event(event)

        settings_ui.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
