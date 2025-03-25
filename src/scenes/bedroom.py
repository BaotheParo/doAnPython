import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Định nghĩa đường dẫn đến ảnh nền
BEDROOM_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-phongngu.png")

class Bedroom:
    def __init__(self, game_state, screen, ui):
        self.game_state = game_state
        self.screen = screen
        self.ui = ui
        pygame.display.set_caption("Phòng ngủ")

        # Load hình ảnh phòng ngủ
        try:
            self.background = pygame.image.load(BEDROOM_IMAGE_PATH).convert()
            self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file - {e}")
            self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            self.background.fill((50, 50, 100))  # Màu nền mặc định nếu không load được

        # Định vị giường và cửa
        self.bed_rect = pygame.Rect(150, 200, 120, 80)  # Vị trí của giường
        self.door_rect = pygame.Rect(500, 200, 80, 120)  # Vị trí của cửa

        # Thêm hình chữ nhật tùy ý để chuyển sang FarmScene
        self.farm_rect = pygame.Rect(300, 400, 100, 50)  # Vị trí và kích thước hình chữ nhật (có thể tùy chỉnh)
        self.farm_text = pygame.font.SysFont(None, 24).render("To Farm", True, (255, 255, 255))
        self.farm_bg = pygame.Surface((100, 50))
        self.farm_bg.fill((50, 50, 50))  # Màu nền mặc định
        self.farm_hover = False

        self.font = pygame.font.SysFont(None, 24)
        self.running = True

    def run(self):
        """Chạy vòng lặp chính của phòng ngủ"""
        clock = pygame.time.Clock()

        while self.running:
            delta_time = clock.tick(60)
            self.game_state.time_system.update(delta_time)

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.interact(mouse_pos)
                    if action == "farm":
                        from src.scenes.farm import FarmScene
                        print("Chuyển đến FarmScene!")
                        self.running = False
                        farm_scene = FarmScene(self.game_state, self.screen, self.ui)
                        farm_scene.run()
                        pygame.display.set_caption("Phòng ngủ")
                        self.running = True
                    elif action == "sleep":
                        print("Người chơi đã ngủ, ngày mới bắt đầu!")

            self.draw(mouse_pos)  # Truyền mouse_pos vào draw
            self.ui.draw()
            pygame.display.flip()

    def draw(self, mouse_pos):
        """Vẽ giao diện phòng ngủ"""
        self.screen.blit(self.background, (0, 0))

        # Hiển thị tọa độ chuột
        coord_text = self.font.render(f"Mouse: {mouse_pos}", True, (255, 255, 255))
        coord_bg = pygame.Surface((150, 25))
        coord_bg.fill((50, 50, 50))
        self.screen.blit(coord_bg, (10, 40))  # Đặt dưới time_text để không che
        self.screen.blit(coord_text, (15, 45))

        # Hiển thị thời gian hiện tại
        time_text = self.font.render(
            f"Day: {self.game_state.time_system.current_day} | {self.game_state.time_system.get_time_of_day()}",
            True, (255, 255, 255)
        )
        time_bg = pygame.Surface((300, 25))
        time_bg.fill((50, 50, 50))
        self.screen.blit(time_bg, (10, 10))
        self.screen.blit(time_text, (15, 15))

        # Vẽ hình chữ nhật "To Farm" với hiệu ứng hover
        self.farm_hover = self.farm_rect.collidepoint(mouse_pos)
        self.farm_bg.fill((100, 100, 100) if self.farm_hover else (50, 50, 50))
        self.screen.blit(self.farm_bg, (self.farm_rect.x, self.farm_rect.y))
        self.screen.blit(self.farm_text, (self.farm_rect.x + 10, self.farm_rect.y + 15))
        pygame.draw.rect(self.screen, (255, 255, 255), self.farm_rect, 2)  # Viền trắng

    def interact(self, pos):
        """Xử lý tương tác khi người chơi nhấn chuột"""
        if self.bed_rect.collidepoint(pos):
            self.game_state.time_system.toggle_day_night()
            return "sleep"  # Người chơi đã ngủ, ngày mới bắt đầu
        elif self.door_rect.collidepoint(pos) or self.farm_rect.collidepoint(pos):
            return "farm"  # Người chơi đi ra nông trại
        return None