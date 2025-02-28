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

        self.bar_x = SCREEN_WIDTH // 2 - FISHING_BAR_WIDTH // 2
        self.bar_y = 50

        self.green_zone_pos = (FISHING_BAR_HEIGHT - self.green_zone_size) // 2 + self.bar_y
        self.green_zone_speed = 0

        self.fish_pos = FISHING_BAR_HEIGHT // 2 + self.bar_y
        self.fish_speed = random.choice([-3, 3])

        self.timer = TIMER_START

        self.running = True
        self.success = False

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.green_zone_speed = -5
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.green_zone_speed = 5

            self.green_zone_pos += self.green_zone_speed
            self.green_zone_pos = max(self.bar_y,
                                      min(self.bar_y + FISHING_BAR_HEIGHT - self.green_zone_size, self.green_zone_pos))

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
                self.running = False
            elif self.timer <= 0:
                self.success = False
                self.running = False

            self.screen.fill(WHITE)
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

            pygame.display.flip()
            clock.tick(60)

        self.player.reduce_energy(ENERGY_COSTS["fish"])
        if self.success:
            self.catch_fish()
        else:
            print("Cá đã thoát mất!")
        # Không gọi pygame.quit() để quay lại fishing.py

    def catch_fish(self):
        fish_list = FISH_DAY if self.time_of_day == "day" else FISH_NIGHT
        caught_fish = random.choice(fish_list)
        self.player.inventory.add_item(caught_fish, 1)
        print(f"Bạn đã câu được: {caught_fish}")


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