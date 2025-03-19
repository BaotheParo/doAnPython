import pygame
import os

# Khởi tạo pygame
pygame.init()

# Định nghĩa đường dẫn đến icon
ICON_PATH = os.path.join("assets", "images", "icons")

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        
        # Load icon
        self.icons = {
            "play": pygame.image.load(os.path.join(ICON_PATH, "play.png")),
            "continue": pygame.image.load(os.path.join(ICON_PATH, "continue.png")),
            "quit": pygame.image.load(os.path.join(ICON_PATH, "quit.png")),
            "laban": pygame.image.load(os.path.join(ICON_PATH, "laban.png")),
            "tuido": pygame.image.load(os.path.join(ICON_PATH, "tuido.png")),
            "map": pygame.image.load(os.path.join(ICON_PATH, "map.png")),
            "setting": pygame.image.load(os.path.join(ICON_PATH, "setting.png")),
            "sang": pygame.image.load(os.path.join(ICON_PATH, "sang.png")),
            "trua": pygame.image.load(os.path.join(ICON_PATH, "trua.png")),
            "chieu": pygame.image.load(os.path.join(ICON_PATH, "chieu.png")),
            "toi": pygame.image.load(os.path.join(ICON_PATH, "toi.png")),
        }

        # Định nghĩa nút bấm với icon
        self.buttons = {
            "play": pygame.Rect(150, 200, 120, 50),
            "continue": pygame.Rect(300, 200, 120, 50),
            "quit": pygame.Rect(450, 200, 120, 50),
            "laban": pygame.Rect(150, 300, 50, 50),
            "tuido": pygame.Rect(250, 300, 50, 50),
            "map": pygame.Rect(350, 300, 50, 50),
            "setting": pygame.Rect(450, 300, 50, 50),
        }

        # Vị trí icon thời gian (mặc định là sáng)
        self.time_status = "sang"

    def draw(self):
        """Vẽ giao diện menu"""
        self.screen.fill((50, 50, 50))  # Nền màu xám đậm
        
        # Vẽ các nút bấm
        for key, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), rect, border_radius=10)
            self.screen.blit(self.icons[key], (rect.x + 10, rect.y + 5))

        # Hiển thị icon thời gian
        time_icon = self.icons[self.time_status]
        self.screen.blit(time_icon, (700, 50))  # Hiển thị góc trên phải

        pygame.display.flip()

    def handle_click(self, pos):
        """Xử lý khi người chơi nhấn vào nút"""
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return key
        return None

    def update_time_status(self, new_status):
        """Cập nhật trạng thái thời gian (sáng, trưa, chiều, tối)"""
        if new_status in self.icons:
            self.time_status = new_status
