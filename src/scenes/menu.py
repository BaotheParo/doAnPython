import pygame
import os

# Khởi tạo pygame
pygame.init()

# Định nghĩa đường dẫn đến icon
ICON_PATH = os.path.join("assets", "images", "icons")

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Tọa độ hiển thị icon thời gian
TIME_ICON_POS = (SCREEN_WIDTH - 100, 50)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

        # Load icon với kiểm tra lỗi
        self.icons = {}
        icon_names = ["play", "continue", "quit", "laban", "tuido", "map", "setting", "sang", "trua", "chieu", "toi"]
        
        for name in icon_names:
            path = os.path.join(ICON_PATH, f"{name}.png")
            if os.path.exists(path):
                self.icons[name] = pygame.image.load(path)
            else:
                print(f"Warning: Icon {name}.png not found!")
                self.icons[name] = pygame.Surface((50, 50))  # Placeholder nếu thiếu

        # Định nghĩa nút bấm với icon
        self.buttons = {
            "play": pygame.Rect(300, 250, 150, 60),
            "continue": pygame.Rect(500, 250, 150, 60),
            "quit": pygame.Rect(700, 250, 150, 60),
            "laban": pygame.Rect(300, 400, 60, 60),
            "tuido": pygame.Rect(450, 400, 60, 60),
            "map": pygame.Rect(600, 400, 60, 60),
            "setting": pygame.Rect(750, 400, 60, 60),
        }

        # Vị trí icon thời gian (mặc định là sáng)
        self.time_status = "sang"

        # Âm thanh click (nếu có file âm thanh)
        sound_path = os.path.join("assets", "sounds", "click.wav")
        self.click_sound = pygame.mixer.Sound(sound_path) if os.path.exists(sound_path) else None

    def draw(self):
        """Vẽ giao diện menu"""
        self.screen.fill((50, 50, 50))  # Nền màu xám đậm
        
        # Vẽ các nút bấm
        for key, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), rect, border_radius=10)
            if key in self.icons:
                icon = self.icons[key]
                icon_x = rect.x + (rect.width - icon.get_width()) // 2  # Căn giữa icon
                icon_y = rect.y + (rect.height - icon.get_height()) // 2
                self.screen.blit(icon, (icon_x, icon_y))

        # Hiển thị icon thời gian
        time_icon = self.icons.get(self.time_status, pygame.Surface((50, 50)))  # Nếu thiếu, tạo placeholder
        self.screen.blit(time_icon, TIME_ICON_POS)  # Dùng hằng số

        pygame.display.flip()

    def handle_click(self, pos):
        """Xử lý khi người chơi nhấn vào nút"""
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if self.click_sound:
                    self.click_sound.play()  # Phát âm thanh khi click
                return key
        return None

    def update_time_status(self, new_status):
        """Cập nhật trạng thái thời gian (sáng, trưa, chiều, tối)"""
        if new_status in self.icons:
            self.time_status = new_status

