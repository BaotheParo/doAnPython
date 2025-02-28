import pygame
from src.core.player import Player
from src.actions.fishing_action import start_fishing
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


# Không khởi tạo pygame.init() ở đây, sẽ khởi tạo trong main.py

class FishingScene:
    def __init__(self, player, time_system, screen):
        self.player = player
        self.time_system = time_system
        self.screen = screen
        pygame.display.set_caption("Khu vực câu cá")

        background_path = "../../assets/images/backgrounds/background-cauca.png"
        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.lake_rect = pygame.Rect(300, 200, 200, 150)
        self.home_sign_rect = pygame.Rect(50, 500, 100, 50)
        self.village_sign_rect = pygame.Rect(650, 500, 100, 50)

        self.hover_color = (200, 200, 200, 128)
        self.hover_surface = pygame.Surface((self.lake_rect.width, self.lake_rect.height), pygame.SRCALPHA)
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

            self.screen.blit(self.background, (0, 0))
            if self.lake_rect.collidepoint(mouse_pos):
                self.screen.blit(self.hover_surface, (self.lake_rect.x, self.lake_rect.y))

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        if self.lake_rect.collidepoint(pos):
            print("Bắt đầu câu cá!")
            start_fishing(self.player, self.time_system.get_time_of_day(), self.screen)  # Chạy minigame
            print("Quay lại khu vực câu cá!")  # Thông báo sau khi minigame kết thúc
        elif self.home_sign_rect.collidepoint(pos):
            print("Quay về phòng ngủ!")
            self.running = False
        elif self.village_sign_rect.collidepoint(pos):
            print("Đi đến làng!")
            self.running = False


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    from src.core.player import Player


    class FakeTimeSystem:
        def get_time_of_day(self):
            return "day"


    player = Player()
    time_system = FakeTimeSystem()
    fishing_scene = FishingScene(player, time_system, screen)
    fishing_scene.run()
    pygame.quit()