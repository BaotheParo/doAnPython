import pygame
from src.core.player import Player
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

# Không khởi tạo pygame.init() ở đây, sẽ khởi tạo trong main.py

class VillageScene:
    def __init__(self, player, time_system, screen):
        self.player = player
        self.time_system = time_system
        self.screen = screen
        pygame.display.set_caption("Khu vực làng")

        # Đường dẫn đến các file background
        self.day_background_path = "D:/Python game/doAnPython/assets/images/backgrounds/background-ngoilang.png"
        self.night_background_path = "D:/Python game/doAnPython/assets/images/backgrounds/background-ngoilang-dem.png"

        try:
            # Tải và scale background ban ngày
            self.day_background = pygame.image.load(self.day_background_path).convert()
            self.day_background = pygame.transform.scale(self.day_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

            # Tải và scale background ban đêm
            self.night_background = pygame.image.load(self.night_background_path).convert()
            self.night_background = pygame.transform.scale(self.night_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file - {e}")
            raise

        # Khu vực tương tác
        self.fishing_sign_rect = pygame.Rect(300, 200, 200, 150)  # Đi đến khu vực câu cá
        self.home_sign_rect = pygame.Rect(50, 500, 100, 50)      # Quay về nhà
        self.market_sign_rect = pygame.Rect(650, 500, 100, 50)    # Đi đến chợ

        # Hiệu ứng hover
        self.hover_color = (200, 200, 200, 128)
        self.hover_surface = pygame.Surface((self.fishing_sign_rect.width, self.fishing_sign_rect.height), pygame.SRCALPHA)
        self.hover_surface.fill(self.hover_color)

        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(mouse_pos)

            # Chọn background dựa trên thời gian
            time_of_day = self.time_system.get_time_of_day()
            if time_of_day == "day":
                self.screen.blit(self.day_background, (0, 0))
            elif time_of_day == "night":
                self.screen.blit(self.night_background, (0, 0))

            # Hiệu ứng hover khi chuột di qua khu vực câu cá
            if self.fishing_sign_rect.collidepoint(mouse_pos):
                self.screen.blit(self.hover_surface, (self.fishing_sign_rect.x, self.fishing_sign_rect.y))

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        if self.fishing_sign_rect.collidepoint(pos):
            print("Đi đến khu vực câu cá!")
            self.running = False  # Thoát để chuyển scene (sẽ xử lý trong main.py)
        elif self.home_sign_rect.collidepoint(pos):
            print("Quay về phòng ngủ!")
            self.running = False
        elif self.market_sign_rect.collidepoint(pos):
            print("Đi đến chợ!")
            self.running = False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    from src.core.player import Player

    class FakeTimeSystem:
        def get_time_of_day(self):
            return "night"  # Thay thành "night" để kiểm tra ban đêm

    player = Player()
    time_system = FakeTimeSystem()
    village_scene = VillageScene(player, time_system, screen)
    village_scene.run()
    pygame.quit()