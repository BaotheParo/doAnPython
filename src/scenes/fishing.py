import pygame
from src.core.player import Player
from src.actions.fishing_action import start_fishing
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class FishingScene:
    def __init__(self, player, time_system, screen):
        self.player = player
        self.time_system = time_system
        self.screen = screen
        pygame.display.set_caption("Khu vực câu cá")

        # Đường dẫn đến các file background
        self.day_background_path = "../../assets/images/backgrounds/background-cauca.png"
        self.night_background_path = "../../assets/images/backgrounds/background-cauca-dem.png"

        # Tải và scale background ban ngày
        self.day_background = pygame.image.load(self.day_background_path).convert()
        self.day_background = pygame.transform.scale(self.day_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Tải và scale background ban đêm
        self.night_background = pygame.image.load(self.night_background_path).convert()
        self.night_background = pygame.transform.scale(self.night_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Chỉ giữ lake_rect
        self.lake_rect = pygame.Rect(515, 450, 485, 200)  # (x, y, width, height)

        # Cập nhật hover_surface để khớp với kích thước của lake_rect
        self.hover_color = (200, 200, 200, 10)
        self.hover_surface = pygame.Surface((self.lake_rect.width, self.lake_rect.height), pygame.SRCALPHA)
        self.hover_surface.fill(self.hover_color)

        # Font để hiển thị tọa độ chuột
        self.font = pygame.font.SysFont(None, 24)

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

            # Kiểm tra thời gian để chọn background
            time_of_day = self.time_system.get_time_of_day()
            if time_of_day == "day":
                self.screen.blit(self.day_background, (0, 0))
            elif time_of_day == "night":
                self.screen.blit(self.night_background, (0, 0))

            # Vẽ hiệu ứng hover khi chuột di qua hồ nước
            if self.lake_rect.collidepoint(mouse_pos):
                self.screen.blit(self.hover_surface, (self.lake_rect.x, self.lake_rect.y))

            # Hiển thị tọa độ chuột trên màn hình
            coord_text = self.font.render(f"X: {mouse_pos[0]}, Y: {mouse_pos[1]}", True, WHITE)
            self.screen.blit(coord_text, (10, 10))  # Vẽ tọa độ ở góc trên cùng bên trái

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        if self.lake_rect.collidepoint(pos):
            print("Bắt đầu câu cá!")
            start_fishing(self.player, self.time_system.get_time_of_day(), self.screen)  # Chạy minigame
            print("Quay lại khu vực câu cá!")  # Thông báo sau khi minigame kết thúc)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    from src.core.player import Player

    class FakeTimeSystem:
        def get_time_of_day(self):
            return "night"  # Thay đổi thành "night" để kiểm tra background ban đêm

    player = Player()
    time_system = FakeTimeSystem()
    fishing_scene = FishingScene(player, time_system, screen)
    fishing_scene.run()
    pygame.quit()