import pygame
from src.core.player import Player
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.scenes.thuongnhannongtrai import ThuongNhanNongTraiScene  # Import ThuongNhanNongTraiScene
from src.scenes.fishing import FishingScene  # Import FishingScene

class VillageScene:
    def __init__(self, player, time_system, screen):
        self.player = player
        self.time_system = time_system
        self.screen = screen
        pygame.display.set_caption("Khu vực làng")

        # Đường dẫn đến các file background (đường dẫn tương đối)
        self.day_background_path = "../../assets/images/backgrounds/background-ngoilang.png"
        self.night_background_path = "../../assets/images/backgrounds/background-ngoilang-dem.png"

        try:
            self.day_background = pygame.image.load(self.day_background_path).convert()
            self.day_background = pygame.transform.scale(self.day_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_background = pygame.image.load(self.night_background_path).convert()
            self.night_background = pygame.transform.scale(self.night_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file - {e}")
            self.day_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.day_background.fill((100, 200, 100))
            self.night_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_background.fill((0, 0, 50))

        # Các khu vực tương tác
        self.farmer_trader_rect = pygame.Rect(200, 400, 100, 50)  # Thương nhân nông trại
        self.fisher_trader_rect = pygame.Rect(350, 400, 100, 50)  # Thương nhân câu cá
        self.home_sign_rect = pygame.Rect(500, 400, 100, 50)      # Biển hiệu đến nhà
        self.lake_sign_rect = pygame.Rect(650, 400, 100, 50)      # Biển hiệu đến ao

        # Hiệu ứng hover
        self.hover_color = (200, 200, 200, 128)
        self.hover_surface = pygame.Surface((100, 50), pygame.SRCALPHA)
        self.hover_surface.fill(self.hover_color)

        # Tooltip
        self.tooltip_font = pygame.font.SysFont(None, 25)
        self.tooltips = {
            "farmer_trader": self.tooltip_font.render("Thương nhân nông trại", True, WHITE),
            "fisher_trader": self.tooltip_font.render("Thương nhân câu cá", True, WHITE),
            "home_sign": self.tooltip_font.render("Đi đến nhà", True, WHITE),
            "lake_sign": self.tooltip_font.render("Đi đến ao", True, WHITE)
        }
        self.tooltip_bg = pygame.Surface((150, 35))
        self.tooltip_bg.fill((50, 50, 50))

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

            # Vẽ background
            time_of_day = self.time_system.get_time_of_day()
            if time_of_day == "day":
                self.screen.blit(self.day_background, (0, 0))
            elif time_of_day == "night":
                self.screen.blit(self.night_background, (0, 0))

            # Hiệu ứng hover và tooltip
            for rect, name in [(self.farmer_trader_rect, "farmer_trader"),
                              (self.fisher_trader_rect, "fisher_trader"),
                              (self.home_sign_rect, "home_sign"),
                              (self.lake_sign_rect, "lake_sign")]:
                if rect.collidepoint(mouse_pos):
                    self.screen.blit(self.hover_surface, rect.topleft)
                    tooltip_x = rect.x
                    tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                    self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                    self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        if self.farmer_trader_rect.collidepoint(pos):
            print("Đi đến thương nhân nông trại!")
            trader_scene = ThuongNhanNongTraiScene(self.player, self.time_system, self.screen)
            trader_scene.run()
        elif self.fisher_trader_rect.collidepoint(pos):
            print("Mở menu thương nhân câu cá!")  # Có thể chuyển sang scene khác nếu muốn
            # Ví dụ: trader_fish_scene = ThuongNhanCauluaScene(self.player, self.time_system, self.screen)
        elif self.home_sign_rect.collidepoint(pos):
            print("Đi đến nhà!")
            self.running = False
        elif self.lake_sign_rect.collidepoint(pos):
            print("Đi đến ao câu cá!")
            fishing_scene = FishingScene(self.player, self.time_system, self.screen)
            fishing_scene.run()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    from src.core.player import Player

    class FakeTimeSystem:
        def get_time_of_day(self):
            return "day"

    player = Player()
    player.add_money(50)  # Thêm tiền để thử nghiệm
    time_system = FakeTimeSystem()
    village_scene = VillageScene(player, time_system, screen)
    village_scene.run()
    pygame.quit()