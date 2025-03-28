import pygame
import os, sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
IMAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "assets", "images"))

from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Bedroom:
    def __init__(self, game_state, screen, ui):
        self.game_state = game_state
        self.screen = screen
        self.ui = ui  # UI (SettingsUI) được truyền vào
        pygame.display.set_caption("Phòng ngủ")

        # Load hình ảnh phòng ngủ
        try:
            self.background = pygame.image.load(os.path.join(IMAGE_DIR, "backgrounds", "background-phongngu.png")).convert()
            self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file - {e}")
            self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            self.background.fill((50, 50, 100))

        # Định vị giường và cửa
        self.bed_rect = pygame.Rect(150, 200, 120, 80)
        self.door_rect = pygame.Rect(500, 200, 80, 120)

        # Nút chuyển sang FarmScene (vùng "To Farm")
        self.farm_rect = pygame.Rect(300, 400, 100, 50)
        self.farm_text = pygame.font.SysFont(None, 24).render("To Farm", True, (255,255,255))
        self.farm_bg = pygame.Surface((100,50))
        self.farm_bg.fill((50,50,50))
        self.farm_hover = False

        self.font = pygame.font.SysFont(None, 24)
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Nếu cửa sổ thay đổi kích thước, cập nhật lại màn hình và UI
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.ui = self.recreate_ui()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Cho UI xử lý sự kiện trước
                    ui_handled = self.ui.handle_event(event)
                    if not ui_handled:
                        action = self.interact(mouse_pos)
                        if action == "farm":
                            from src.scenes.farm import FarmScene
                            print("Chuyển đến FarmScene!")
                            self.running = False
                            farm_scene = FarmScene(self.game_state, self.screen, self.ui)
                            farm_scene.run()
                        elif action == "sleep":
                            print("Người chơi đã ngủ, ngày mới bắt đầu!")
            self.draw(mouse_pos)
            self.ui.draw()  # Vẽ UI trên cùng
            pygame.display.flip()
            clock.tick(60)

    def draw(self, mouse_pos):
        self.screen.blit(self.background, (0, 0))
        # Vẽ thông tin thời gian và tọa độ
        time_text = self.font.render(f"Day: {self.game_state.time_system.current_day} | {self.game_state.time_system.get_time_of_day()}", True, (255,255,255))
        self.screen.blit(time_text, (15, 15))
        coord_text = self.font.render(f"Mouse: {mouse_pos}", True, (255,255,255))
        self.screen.blit(coord_text, (15, 40))
        # Vẽ nút "To Farm" với hiệu ứng hover
        self.farm_hover = self.farm_rect.collidepoint(mouse_pos)
        self.farm_bg.fill((100,100,100) if self.farm_hover else (50,50,50))
        self.screen.blit(self.farm_bg, (self.farm_rect.x, self.farm_rect.y))
        self.screen.blit(self.farm_text, (self.farm_rect.x + 10, self.farm_rect.y + 15))
        pygame.draw.rect(self.screen, (255,255,255), self.farm_rect, 2)

    def interact(self, pos):
        if self.door_rect.collidepoint(pos) or self.farm_rect.collidepoint(pos):
            return "farm"  # Chuyển đến FarmScene
        elif self.bed_rect.collidepoint(pos):
            return "sleep"  # Người chơi ngủ => bắt đầu ngày mới
        return None

    def recreate_ui(self):
        """Tạo lại UI khi kích thước màn hình thay đổi."""
        from src.core.ui import SettingsUI
        return SettingsUI(self.screen, self.game_state)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    from src.core.game_state import GameState
    from src.core.ui import SettingsUI
    game_state = GameState()
    ui = SettingsUI(screen, game_state)
    bedroom = Bedroom(game_state, screen, ui)
    bedroom.run()
    pygame.quit()
