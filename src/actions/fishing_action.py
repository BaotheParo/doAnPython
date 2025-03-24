import pygame
import random
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
from src.core.player import Player
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED,
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

    def run(self):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 48)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.green_zone_speed = -5
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.green_zone_speed = 5

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
            elif self.result_phase == 1:
                self.screen.blit(self.background_complete, (0, 0))
                self.result_timer += clock.get_time()
                if self.result_timer >= 2000:
                    self.result_phase = 2
                    self.result_timer = 0
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

                self.result_timer += clock.get_time()
                if self.result_timer >= 2000:
                    self.running = False

            pygame.display.flip()
            clock.tick(60)

        self.player.reduce_energy(ENERGY_COSTS["fish"])

    def catch_fish(self):
        # Sửa điều kiện để so sánh với "Ngày" và "Đêm"
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
    if player.reduce_energy(ENERGY_COSTS["fish"]):
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