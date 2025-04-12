import pygame
import random
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
from src.core.player import Player
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, BLUE,
    FISHING_BAR_WIDTH, FISHING_BAR_HEIGHT, FISHING_FISH_SIZE,
    FISHING_GREEN_ZONE_SIZE, ENERGY_COSTS, FISH_DAY, FISH_NIGHT
)

TIMER_WIDTH = 30
TIMER_HEIGHT = 400
TIMER_MAX = 100
TIMER_START = TIMER_MAX // 2
TIMER_SPEED = 0.5

class FishingMinigame:
    def __init__(self, player, time_of_day, screen):
        self.player = player
        self.time_of_day = time_of_day
        self.screen = screen
        self.rod_level = player.get_rod_level()
        self.green_zone_size = FISHING_GREEN_ZONE_SIZE[self.rod_level]

        # In giá trị time_of_day để kiểm tra
        print(f"Time of day: {self.time_of_day}")

        # Tải background cho minigame
        self.background_path1 = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "animation-cauca1.png")
        self.background = pygame.image.load(self.background_path1).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Tải background sau khi hoàn thành (giai đoạn 1)
        self.background_path2 = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "animation-cauca2.png")
        self.background_complete = pygame.image.load(self.background_path2).convert()
        self.background_complete = pygame.transform.scale(self.background_complete, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Tải hình ảnh cho fishing bar (thay thế màu đen)
        self.bar_image_path = os.path.join(BASE_DIR, "assets", "images", "fish", "fishing_bar.png")
        try:
            self.bar_image = pygame.image.load(self.bar_image_path).convert_alpha()
            self.bar_image = pygame.transform.scale(self.bar_image, (FISHING_BAR_WIDTH, FISHING_BAR_HEIGHT))
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.bar_image_path}")
            self.bar_image = pygame.Surface((FISHING_BAR_WIDTH, FISHING_BAR_HEIGHT))
            self.bar_image.fill(BLACK)

        # Tải hình ảnh cho con cá (thay thế màu đỏ)
        self.fish_image_path = os.path.join(BASE_DIR, "assets", "images", "fish", "fish.png")
        try:
            self.fish_image = pygame.image.load(self.fish_image_path).convert_alpha()
            self.fish_image = pygame.transform.scale(self.fish_image, (FISHING_FISH_SIZE, FISHING_FISH_SIZE))
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.fish_image_path}")
            self.fish_image = pygame.Surface((FISHING_FISH_SIZE, FISHING_FISH_SIZE))
            self.fish_image.fill(RED)

        # Tải hình ảnh cho thanh xanh lá (thay thế màu GREEN)
        self.green_zone_image_path = os.path.join(BASE_DIR, "assets", "images", "green_zone.png")
        try:
            self.green_zone_image = pygame.image.load(self.green_zone_image_path).convert_alpha()
            self.green_zone_image = pygame.transform.scale(self.green_zone_image,
                                                           (FISHING_BAR_WIDTH - 50, self.green_zone_size))
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.green_zone_image_path}")
            self.green_zone_image = pygame.Surface((FISHING_BAR_WIDTH - 15, self.green_zone_size))
            self.green_zone_image.fill(GREEN)

        # Tải hình ảnh cho khung bao quanh thanh đen
        self.border_path = os.path.join(BASE_DIR, "assets", "images", "fish", "Picture2.png")
        try:
            self.border_image = pygame.image.load(self.border_path).convert_alpha()
            self.border_image = pygame.transform.scale(self.border_image, (150, 450))
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.border_path}")
            self.border_image = pygame.Surface((FISHING_BAR_WIDTH, self.green_zone_size))
            self.border_image.fill(GREEN)

        # Tải hình ảnh khung cho kết quả (khi bắt được cá)
        self.result_frame_path = os.path.join(BASE_DIR, "assets", "images", "fish", "Picture3.png")
        try:
            self.result_frame = pygame.image.load(self.result_frame_path).convert_alpha()
            self.result_frame = pygame.transform.scale(self.result_frame, (850, 400))
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.result_frame_path}")
            self.result_frame = None

        # Thiết lập thanh thể lực (mana bar)
        self.MANA_BAR_WIDTH = 600
        self.MANA_BAR_HEIGHT = 30
        self.MANA_BAR_X = (SCREEN_WIDTH - self.MANA_BAR_WIDTH) // 2
        self.MANA_BAR_Y = SCREEN_HEIGHT - 50

        # Thiết lập font
        self.font = pygame.font.SysFont(None, 24)
        self.button_font = pygame.font.SysFont(None, 36)

        # Thiết lập biểu tượng quay lại (icon-quaylai.png) cho màn hình xác nhận và minigame
        self.back_icon_path = os.path.join(BASE_DIR, "assets", "images", "icons", "icon-quaylai.png")
        try:
            self.back_icon = pygame.image.load(self.back_icon_path).convert_alpha()
            self.back_icon = pygame.transform.scale(self.back_icon, (60, 60))  # Kích thước 60x60
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.back_icon_path}")
            self.back_icon = pygame.Surface((60, 60))
            self.back_icon.fill((160, 150, 150))  # Màu xám nếu không tìm thấy hình ảnh
        self.back_button_rect = pygame.Rect(SCREEN_WIDTH - 70, 10, 60, 60)  # Đặt ở góc trên bên phải

        # Thiết lập nút "Có" (Yes) cho màn hình xác nhận
        self.yes_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50, 120, 40)
        self.yes_button_text = self.button_font.render("Có", True, WHITE)
        self.yes_button_bg = pygame.Surface((120, 40))
        self.yes_button_bg.fill((50, 150, 50))  # Màu xanh lá cho nút "Có"

        # Thiết lập nút chơi lại (Replay) ở giai đoạn kết quả
        self.replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 150, 120, 40)
        self.replay_button_text = self.button_font.render("Chơi lại", True, WHITE)
        self.replay_button_bg = pygame.Surface((120, 40))
        self.replay_button_bg.fill((50, 150, 50))  # Màu xanh lá cho nút chơi lại

        # Trạng thái ban đầu
        self.confirmation_phase = True  # Thêm trạng thái cho màn hình xác nhận
        self.has_played = False  # Biến để kiểm tra xem người chơi đã bắt đầu minigame chưa
        self.reset_game()

    def reset_game(self):
        """Reset trạng thái của minigame để chơi lại từ đầu."""
        self.bar_x = 85
        self.bar_y = 50
        self.bar_x_border = 28
        self.bar_y_border = 35
        self.green_zone_pos = (FISHING_BAR_HEIGHT - self.green_zone_size) // 2 + self.bar_y
        self.green_zone_speed = 0

        self.fish_pos = FISHING_BAR_HEIGHT // 2 + self.bar_y
        self.fish_speed = random.choice([-3, 3])

        self.timer = TIMER_START

        self.running = True
        self.success = False
        self.result_phase = 0
        self.result_timer = 0
        self.caught_fish = None
        self.caught_fish_image = None

    def draw_mana_bar(self):
        """Vẽ thanh thể lực (mana bar) lên màn hình."""
        pygame.draw.rect(self.screen, BLACK, (self.MANA_BAR_X - 5, self.MANA_BAR_Y - 5, self.MANA_BAR_WIDTH + 10, self.MANA_BAR_HEIGHT + 10), border_radius=5)
        pygame.draw.rect(self.screen, WHITE, (self.MANA_BAR_X, self.MANA_BAR_Y, self.MANA_BAR_WIDTH, self.MANA_BAR_HEIGHT), border_radius=5)
        mana_width = (self.player.get_energy() / self.player.max_energy) * (self.MANA_BAR_WIDTH - 4)
        pygame.draw.rect(self.screen, BLUE, (self.MANA_BAR_X + 2, self.MANA_BAR_Y + 2, mana_width, self.MANA_BAR_HEIGHT - 4), border_radius=5)
        energy_text = self.font.render(f"MANA: {self.player.get_energy()}/{self.player.max_energy}", True, BLACK)
        self.screen.blit(energy_text, (self.MANA_BAR_X + (self.MANA_BAR_WIDTH - energy_text.get_width()) // 2, self.MANA_BAR_Y + (self.MANA_BAR_HEIGHT - energy_text.get_height()) // 2))

    def draw_confirmation_screen(self):
        """Vẽ màn hình xác nhận trước khi bắt đầu minigame."""
        # Vẽ background
        self.screen.blit(self.background, (0, 0))

        # Vẽ thông báo
        confirm_text = self.button_font.render("Bạn có muốn câu cá không?", True, WHITE)
        confirm_rect = confirm_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(self.screen, BLACK, confirm_rect.inflate(20, 20))
        self.screen.blit(confirm_text, confirm_rect)

        # Vẽ nút "Có"
        self.screen.blit(self.yes_button_bg, (self.yes_button_rect.x, self.yes_button_rect.y))
        self.screen.blit(self.yes_button_text, (self.yes_button_rect.x + 35, self.yes_button_rect.y + 5))

        # Vẽ biểu tượng quay lại
        self.screen.blit(self.back_icon, (self.back_button_rect.x, self.back_button_rect.y))

        # Vẽ thanh thể lực
        self.draw_mana_bar()

    def run(self):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 48)

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Xử lý màn hình xác nhận
                    if self.confirmation_phase:
                        # Nhấp vào nút "Có" để bắt đầu minigame
                        if self.yes_button_rect.collidepoint(mouse_pos):
                            self.confirmation_phase = False
                            self.has_played = True  # Đánh dấu rằng người chơi đã bắt đầu minigame
                            print("Bắt đầu minigame câu cá!")
                        # Nhấp vào biểu tượng quay lại để thoát
                        if self.back_button_rect.collidepoint(mouse_pos):
                            print("Thoát minigame câu cá!")
                            self.running = False
                            break
                    # Xử lý trong minigame
                    else:
                        # Xử lý nhấp chuột vào biểu tượng quay lại trong minigame
                        if self.back_button_rect.collidepoint(mouse_pos):
                            print("Thoát minigame câu cá!")
                            self.running = False
                            break
                        # Xử lý nhấp chuột vào nút chơi lại (chỉ trong giai đoạn kết quả)
                        if self.result_phase == 2 and self.replay_button_rect.collidepoint(mouse_pos):
                            if self.player.get_energy() >= ENERGY_COSTS["fish"]:
                                print("Chơi lại minigame câu cá!")
                                self.reset_game()
                                self.has_played = True  # Đánh dấu rằng người chơi đã chơi lại
                            else:
                                print("Không đủ năng lượng để chơi lại!")
                                self.running = False
                                break
                        # Xử lý điều khiển thanh xanh lá
                        if self.result_phase == 0:
                            self.green_zone_speed = -5
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not self.confirmation_phase and self.result_phase == 0:
                        self.green_zone_speed = 5

            # Màn hình xác nhận
            if self.confirmation_phase:
                self.draw_confirmation_screen()
            else:
                # Logic minigame
                if self.result_phase == 0:
                    self.green_zone_pos += self.green_zone_speed
                    self.green_zone_pos = max(self.bar_y, min(self.bar_y + FISHING_BAR_HEIGHT - self.green_zone_size,
                                                              self.green_zone_pos))

                    self.fish_pos += self.fish_speed
                    if (self.fish_pos - FISHING_FISH_SIZE // 2 <= self.bar_y or
                            self.fish_pos + FISHING_FISH_SIZE // 2 >= self.bar_y + FISHING_BAR_HEIGHT):
                        self.fish_speed = -self.fish_speed
                    else:
                        if random.random() < 0.2:
                            self.fish_speed = random.choice([-3, 3])
                    self.fish_pos = max(self.bar_y + FISHING_FISH_SIZE // 2,
                                        min(self.bar_y + FISHING_BAR_HEIGHT - FISHING_FISH_SIZE // 2, self.fish_pos))

                    fish_center = self.fish_pos
                    green_top = self.green_zone_pos
                    green_bottom = self.green_zone_pos + self.green_zone_size
                    if green_top <= fish_center <= green_bottom:
                        self.timer += TIMER_SPEED
                    else:
                        self.timer -= TIMER_SPEED

                    self.timer = max(0, min(TIMER_MAX, self.timer))

                    if self.timer >= TIMER_MAX:
                        self.success = True
                        self.result_phase = 1
                        self.catch_fish()
                    elif self.timer <= 0:
                        self.success = False
                        self.result_phase = 1

                if self.result_phase == 0:
                    self.screen.blit(self.background, (0, 0))
                    timer_x = 147
                    timer_y = 52
                    timer_height = int((self.timer / TIMER_MAX) * TIMER_HEIGHT)
                    pygame.draw.rect(self.screen, BLACK, (timer_x, timer_y, TIMER_WIDTH, TIMER_HEIGHT), 2)
                    pygame.draw.rect(self.screen, GREEN,
                                     (timer_x, timer_y + TIMER_HEIGHT - timer_height, TIMER_WIDTH, timer_height))

                    self.screen.blit(self.bar_image, (self.bar_x, self.bar_y))
                    self.screen.blit(self.border_image, (self.bar_x_border, self.bar_y_border))
                    self.screen.blit(self.green_zone_image, (self.bar_x + 8, self.green_zone_pos))
                    fish_x = self.bar_x + (FISHING_BAR_WIDTH - FISHING_FISH_SIZE) // 2
                    fish_y = self.fish_pos - FISHING_FISH_SIZE // 2
                    self.screen.blit(self.fish_image, (fish_x, fish_y))

                    # Vẽ thanh thể lực trong giai đoạn chơi
                    self.draw_mana_bar()

                elif self.result_phase == 1:
                    self.screen.blit(self.background_complete, (0, 0))
                    self.result_timer += clock.get_time()
                    if self.result_timer >= 2000:
                        self.result_phase = 2
                        self.result_timer = 0

                    # Vẽ thanh thể lực trong giai đoạn chuyển tiếp
                    self.draw_mana_bar()

                elif self.result_phase == 2:
                    self.screen.blit(self.background_complete, (0, 0))

                    if self.result_frame:
                        frame_x = (SCREEN_WIDTH - self.result_frame.get_width()) // 2
                        frame_y = (SCREEN_HEIGHT - self.result_frame.get_height()) // 2 - 50
                        self.screen.blit(self.result_frame, (frame_x, frame_y))

                    if self.success and self.caught_fish_image:
                        fish_x = (SCREEN_WIDTH - self.caught_fish_image.get_width()) // 2
                        fish_y = (SCREEN_HEIGHT - self.caught_fish_image.get_height()) // 2 - 50
                        self.screen.blit(self.caught_fish_image, (fish_x, fish_y))
                        text = font.render(f"Bạn đã bắt được: {self.caught_fish}", True, WHITE)
                        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                        self.screen.blit(text, text_rect)
                    else:
                        text = font.render("Cá đã thoát mất!", True, WHITE)
                        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                        self.screen.blit(text, text_rect)

                    # Vẽ nút chơi lại
                    self.screen.blit(self.replay_button_bg, (self.replay_button_rect.x, self.replay_button_rect.y))
                    self.screen.blit(self.replay_button_text, (self.replay_button_rect.x + 10, self.replay_button_rect.y + 5))

                    # Vẽ thanh thể lực trong giai đoạn kết quả
                    self.draw_mana_bar()

                # Vẽ biểu tượng quay lại trong minigame
                self.screen.blit(self.back_icon, (self.back_button_rect.x, self.back_button_rect.y))

            pygame.display.flip()
            clock.tick(60)

        # Trừ năng lượng chỉ khi người chơi đã thực sự chơi minigame
        if self.has_played:
            self.player.reduce_energy(ENERGY_COSTS["fish"])
            print(f"Đã trừ {ENERGY_COSTS['fish']} năng lượng. Năng lượng hiện tại: {self.player.get_energy()}")

    def catch_fish(self):
        """Xử lý việc bắt cá và cập nhật inventory."""
        fish_list = FISH_DAY if self.time_of_day == "Ngày" else FISH_NIGHT
        self.caught_fish = random.choice(fish_list)
        self.player.inventory.add_item(self.caught_fish, 1)

        fish_images = {
            "catfish": "caTre.png",
            "carp": "caChep.png",
            "frog": "ech.png",
            "ghost_fish": "caMa.png",
            "eel": "caChinh.png",
            "tilapia": "caRoPhi.png"
        }
        fish_image_name = fish_images.get(self.caught_fish, "caRoPhi.png")
        fish_image_path = os.path.join(BASE_DIR, "assets", "images", "fish", fish_image_name)
        self.caught_fish_image = pygame.image.load(fish_image_path).convert_alpha()
        self.caught_fish_image = pygame.transform.scale(self.caught_fish_image, (200, 200))

        print(f"Bạn đã câu được: {self.caught_fish}")

def start_fishing(player, time_of_day, screen):
    # Kiểm tra năng lượng trước khi khởi tạo minigame
    if player.get_energy() >= ENERGY_COSTS["fish"]:
        minigame = FishingMinigame(player, time_of_day, screen)
        minigame.run()
    else:
        print("Không đủ năng lượng để câu cá!")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player()
    player.energy = 100
    start_fishing(player, "day", screen)
    pygame.quit()