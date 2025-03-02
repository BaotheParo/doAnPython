import pygame
import random
from src.core.player import Player
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED,
    FISHING_BAR_WIDTH, FISHING_BAR_HEIGHT, FISHING_FISH_SIZE,
    FISHING_GREEN_ZONE_SIZE, ENERGY_COSTS, FISH_DAY, FISH_NIGHT
)

# Không khởi tạo pygame.init() ở đây

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

        # Tải background cho minigame
        self.background_path1 = "D:/Python game/doAnPython/assets/images/backgrounds/animation-cauca1.png"
        self.background = pygame.image.load(self.background_path1).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Tải background sau khi hoàn thành (giai đoạn 1)
        self.background_path2 = "D:/Python game/doAnPython/assets/images/backgrounds/animation-cauca2.png"
        self.background_complete = pygame.image.load(self.background_path2).convert()
        self.background_complete = pygame.transform.scale(self.background_complete, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.bar_x = SCREEN_WIDTH // 2 - FISHING_BAR_WIDTH // 2
        self.bar_y = 50

        self.green_zone_pos = (FISHING_BAR_HEIGHT - self.green_zone_size) // 2 + self.bar_y
        self.green_zone_speed = 0

        self.fish_pos = FISHING_BAR_HEIGHT // 2 + self.bar_y
        self.fish_speed = random.choice([-3, 3])

        self.timer = TIMER_START

        self.running = True
        self.success = False
        self.result_phase = 0  # 0: minigame, 1: animation-cauca2, 2: kết quả cá
        self.result_timer = 0
        self.caught_fish = None
        self.fish_image = None  # Sẽ tải trong catch_fish()

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
                # Logic minigame
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

            # Vẽ giao diện
            if self.result_phase == 0:
                # Vẽ minigame
                self.screen.blit(self.background, (0, 0))
                timer_x = 50
                timer_y = 50
                timer_height = int((self.timer / TIMER_MAX) * TIMER_HEIGHT)
                pygame.draw.rect(self.screen, BLACK, (timer_x, timer_y, TIMER_WIDTH, TIMER_HEIGHT), 2)
                pygame.draw.rect(self.screen, GREEN,
                                 (timer_x, timer_y + TIMER_HEIGHT - timer_height, TIMER_WIDTH, timer_height))

                pygame.draw.rect(self.screen, BLACK, (self.bar_x, self.bar_y, FISHING_BAR_WIDTH, FISHING_BAR_HEIGHT))
                pygame.draw.rect(self.screen, GREEN,
                                 (self.bar_x, self.green_zone_pos, FISHING_BAR_WIDTH, self.green_zone_size))
                pygame.draw.rect(self.screen, RED, (self.bar_x + (FISHING_BAR_WIDTH - FISHING_FISH_SIZE) // 2,
                                                    self.fish_pos - FISHING_FISH_SIZE // 2, FISHING_FISH_SIZE,
                                                    FISHING_FISH_SIZE))
            elif self.result_phase == 1:
                # Giai đoạn 1: Hiển thị animation-cauca2.png
                self.screen.blit(self.background_complete, (0, 0))
                self.result_timer += clock.get_time()
                if self.result_timer >= 2000:  # Sau 2 giây
                    self.result_phase = 2
                    self.result_timer = 0
            elif self.result_phase == 2:
                # Giai đoạn 2: Hiển thị kết quả với background animation-cauca2.png
                self.screen.blit(self.background_complete, (0, 0))  # Giữ animation-cauca2 làm nền
                if self.success and self.fish_image:
                    fish_x = (SCREEN_WIDTH - self.fish_image.get_width()) // 2
                    fish_y = (SCREEN_HEIGHT - self.fish_image.get_height()) // 2 - 50
                    self.screen.blit(self.fish_image, (fish_x, fish_y))
                    text = font.render(f"Bạn đã bắt được: {self.caught_fish}", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                    self.screen.blit(text, text_rect)
                else:
                    text = font.render("Cá đã thoát mất!", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    self.screen.blit(text, text_rect)

                self.result_timer += clock.get_time()
                if self.result_timer >= 2000:  # Sau 2 giây nữa
                    self.running = False

            pygame.display.flip()
            clock.tick(60)

        self.player.reduce_energy(ENERGY_COSTS["fish"])

    def catch_fish(self):
        fish_list = FISH_DAY if self.time_of_day == "day" else FISH_NIGHT
        self.caught_fish = random.choice(fish_list)
        self.player.inventory.add_item(self.caught_fish, 1)

        # Tải hình ảnh cá dựa trên loại cá bắt được
        fish_images = {
            "catfish": "caTre.png",
            "carp": "caChep.png",
            "frog": "ech.png",
            "ghost_fish": "caMa.png",
            "eel": "caChinh.png",
            "tilapia": "caRoPhi.png"
        }
        fish_image_name = fish_images.get(self.caught_fish, "caRoPhi.png")  # Mặc định là caRoPhi nếu không tìm thấy
        fish_image_path = f"D:/Python game/doAnPython/assets/images/fish/{fish_image_name}"
        self.fish_image = pygame.image.load(fish_image_path).convert_alpha()
        self.fish_image = pygame.transform.scale(self.fish_image, (200, 200))

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