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

        # Load background for minigame
        self.background_path1 = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "animation-cauca1.png")
        self.background = pygame.image.load(self.background_path1).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load background for completion
        self.background_path2 = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "animation-cauca2.png")
        self.background_complete = pygame.image.load(self.background_path2).convert()
        self.background_complete = pygame.transform.scale(self.background_complete, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load fishing bar image
        self.bar_image_path = os.path.join(BASE_DIR, "assets", "images", "fish", "fishing_bar.png")
        try:
            self.bar_image = pygame.image.load(self.bar_image_path).convert_alpha()
            self.bar_image = pygame.transform.scale(self.bar_image, (FISHING_BAR_WIDTH, FISHING_BAR_HEIGHT))
        except FileNotFoundError:
            print(f"Error: File not found - {self.bar_image_path}")
            self.bar_image = pygame.Surface((FISHING_BAR_WIDTH, FISHING_BAR_HEIGHT))
            self.bar_image.fill(BLACK)

        # Load fish image
        self.fish_image_path = os.path.join(BASE_DIR, "assets", "images", "fish", "fish.png")
        try:
            self.fish_image = pygame.image.load(self.fish_image_path).convert_alpha()
            self.fish_image = pygame.transform.scale(self.fish_image, (FISHING_FISH_SIZE, FISHING_FISH_SIZE))
        except FileNotFoundError:
            print(f"Error: File not found - {self.fish_image_path}")
            self.fish_image = pygame.Surface((FISHING_FISH_SIZE, FISHING_FISH_SIZE))
            self.fish_image.fill(RED)

        # Load green zone image
        self.green_zone_image_path = os.path.join(BASE_DIR, "assets", "images", "green_zone.png")
        try:
            self.green_zone_image = pygame.image.load(self.green_zone_image_path).convert_alpha()
            self.green_zone_image = pygame.transform.scale(self.green_zone_image,
                                                          (FISHING_BAR_WIDTH - 50, self.green_zone_size))
        except FileNotFoundError:
            print(f"Error: File not found - {self.green_zone_image_path}")
            self.green_zone_image = pygame.Surface((FISHING_BAR_WIDTH - 15, self.green_zone_size))
            self.green_zone_image.fill(GREEN)

        # Load border image
        self.border_path = os.path.join(BASE_DIR, "assets", "images", "fish", "Picture2.png")
        try:
            self.border_image = pygame.image.load(self.border_path).convert_alpha()
            self.border_image = pygame.transform.scale(self.border_image, (150, 450))
        except FileNotFoundError:
            print(f"Error: File not found - {self.border_path}")
            self.border_image = pygame.Surface((FISHING_BAR_WIDTH, self.green_zone_size))
            self.border_image.fill(GREEN)

        # Load result frame image
        self.result_frame_path = os.path.join(BASE_DIR, "assets", "images", "fish", "Picture3.png")
        try:
            self.result_frame = pygame.image.load(self.result_frame_path).convert_alpha()
            self.result_frame = pygame.transform.scale(self.result_frame, (850, 400))
        except FileNotFoundError:
            print(f"Error: File not found - {self.result_frame_path}")
            self.result_frame = None

        # Load slipped fish image
        self.slipped_image_path = os.path.join(BASE_DIR, "assets", "images", "fish", "slipped.png")
        try:
            self.slipped_image = pygame.image.load(self.slipped_image_path).convert_alpha()
            self.slipped_image = pygame.transform.scale(self.slipped_image, (200, 200))
        except FileNotFoundError:
            print(f"Error: File not found - {self.slipped_image_path}")
            self.slipped_image = pygame.Surface((200, 200))
            self.slipped_image.fill((100, 100, 100))  # Gray fallback

        # Mana bar setup
        self.MANA_BAR_WIDTH = 600
        self.MANA_BAR_HEIGHT = 30
        self.MANA_BAR_X = (SCREEN_WIDTH - self.MANA_BAR_WIDTH) // 2
        self.MANA_BAR_Y = SCREEN_HEIGHT - 50

        # Fonts
        self.font = pygame.font.SysFont("Arial", 24)
        self.button_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.message_font = pygame.font.SysFont("Arial", 36, bold=True)

        # Back icon setup
        self.back_icon_path = os.path.join(BASE_DIR, "assets", "images", "icons", "icon-quaylai.png")
        try:
            self.back_icon = pygame.image.load(self.back_icon_path).convert_alpha()
            self.back_icon = pygame.transform.scale(self.back_icon, (60, 60))
        except FileNotFoundError:
            print(f"Error: File not found - {self.back_icon_path}")
            self.back_icon = pygame.Surface((60, 60))
            self.back_icon.fill((160, 150, 150))
        self.back_button_rect = pygame.Rect(SCREEN_WIDTH - 70, 10, 60, 60)

        # Yes button for confirmation
        self.yes_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 50, 140, 50)
        self.yes_button_text = self.button_font.render("Yes", True, WHITE)
        self.yes_button_bg = pygame.Surface((140, 50))
        self.yes_button_bg.fill((50, 150, 50))

        # Replay button for result phase
        self.replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 150, 140, 50)
        self.replay_button_text = self.button_font.render("Play Again", True, WHITE)
        self.replay_button_bg = pygame.Surface((140, 50))
        self.replay_button_bg.fill((50, 150, 50))

        # Initial state
        self.confirmation_phase = True
        self.has_played = False
        self.reset_game()

    def reset_game(self):
        """Reset the minigame state to play again."""
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
        """Draw the energy bar on the screen."""
        pygame.draw.rect(self.screen, BLACK, (self.MANA_BAR_X - 5, self.MANA_BAR_Y - 5, self.MANA_BAR_WIDTH + 10, self.MANA_BAR_HEIGHT + 10), border_radius=5)
        pygame.draw.rect(self.screen, WHITE, (self.MANA_BAR_X, self.MANA_BAR_Y, self.MANA_BAR_WIDTH, self.MANA_BAR_HEIGHT), border_radius=5)
        mana_width = (self.player.get_energy() / self.player.max_energy) * (self.MANA_BAR_WIDTH - 4)
        pygame.draw.rect(self.screen, BLUE, (self.MANA_BAR_X + 2, self.MANA_BAR_Y + 2, mana_width, self.MANA_BAR_HEIGHT - 4), border_radius=5)
        energy_text = self.font.render(f"Energy: {self.player.get_energy()}/{self.player.max_energy}", True, BLACK)
        self.screen.blit(energy_text, (self.MANA_BAR_X + (self.MANA_BAR_WIDTH - energy_text.get_width()) // 2, self.MANA_BAR_Y + (self.MANA_BAR_HEIGHT - energy_text.get_height()) // 2))

    def draw_confirmation_screen(self):
        """Draw the confirmation screen before starting the minigame."""
        self.screen.blit(self.background, (0, 0))

        # Draw confirmation message
        confirm_text = self.message_font.render("Would you like to go fishing?", True, WHITE)
        confirm_rect = confirm_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        bg_surface = pygame.Surface((confirm_rect.width + 10, confirm_rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (50, 50, 50, 200), (0, 0, confirm_rect.width + 10, confirm_rect.height + 10), border_radius=10)
        self.screen.blit(bg_surface, (confirm_rect.x - 5, confirm_rect.y - 5))
        self.screen.blit(confirm_text, confirm_rect)

        # Draw Yes button
        self.screen.blit(self.yes_button_bg, (self.yes_button_rect.x, self.yes_button_rect.y))
        yes_text_rect = self.yes_button_text.get_rect(center=self.yes_button_rect.center)
        self.screen.blit(self.yes_button_text, yes_text_rect)

        # Draw back icon
        self.screen.blit(self.back_icon, (self.back_button_rect.x, self.back_button_rect.y))

        # Draw energy bar
        self.draw_mana_bar()

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.confirmation_phase:
                        if self.yes_button_rect.collidepoint(mouse_pos):
                            self.confirmation_phase = False
                            self.has_played = True
                            print("Start Fishing Minigame!")
                        if self.back_button_rect.collidepoint(mouse_pos):
                            print("Exit Fishing Minigame!")
                            self.running = False
                            break
                    else:
                        if self.back_button_rect.collidepoint(mouse_pos):
                            print("Exit Fishing Minigame!")
                            self.running = False
                            break
                        if self.result_phase == 2 and self.replay_button_rect.collidepoint(mouse_pos):
                            if self.player.get_energy() >= ENERGY_COSTS["fish"]:
                                print("Play the fishing mini-game again!")
                                self.reset_game()
                                self.has_played = True
                            else:
                                print("Not enough energy to play again!")
                                self.running = False
                                break
                        if self.result_phase == 0:
                            self.green_zone_speed = -5
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not self.confirmation_phase and self.result_phase == 0:
                        self.green_zone_speed = 5

            if self.confirmation_phase:
                self.draw_confirmation_screen()
            else:
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

                    self.draw_mana_bar()

                elif self.result_phase == 1:
                    self.screen.blit(self.background_complete, (0, 0))
                    self.result_timer += clock.get_time()
                    if self.result_timer >= 2000:
                        self.result_phase = 2
                        self.result_timer = 0
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
                        text = self.message_font.render(f"You caught a {self.caught_fish}!", True, WHITE)
                        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                        bg_surface = pygame.Surface((text_rect.width + 10, text_rect.height + 10), pygame.SRCALPHA)
                        pygame.draw.rect(bg_surface, (50, 50, 50, 200), (0, 0, text_rect.width + 10, text_rect.height + 10), border_radius=10)
                        self.screen.blit(bg_surface, (text_rect.x - 5, text_rect.y - 5))
                        self.screen.blit(text, text_rect)
                    else:
                        # Display slipped image
                        slipped_x = (SCREEN_WIDTH - self.slipped_image.get_width()) // 2
                        slipped_y = (SCREEN_HEIGHT - self.slipped_image.get_height()) // 2 - 50
                        self.screen.blit(self.slipped_image, (slipped_x, slipped_y))
                        text = self.message_font.render("The fish slipped away!", True, WHITE)
                        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                        bg_surface = pygame.Surface((text_rect.width + 10, text_rect.height + 10), pygame.SRCALPHA)
                        pygame.draw.rect(bg_surface, (50, 50, 50, 200), (0, 0, text_rect.width + 10, text_rect.height + 10), border_radius=10)
                        self.screen.blit(bg_surface, (text_rect.x - 5, text_rect.y - 5))
                        self.screen.blit(text, text_rect)

                    # Draw replay button
                    self.screen.blit(self.replay_button_bg, (self.replay_button_rect.x, self.replay_button_rect.y))
                    replay_text_rect = self.replay_button_text.get_rect(center=self.replay_button_rect.center)
                    self.screen.blit(self.replay_button_text, replay_text_rect)

                    self.draw_mana_bar()

                self.screen.blit(self.back_icon, (self.back_button_rect.x, self.back_button_rect.y))

            pygame.display.flip()
            clock.tick(60)

        if self.has_played:
            self.player.reduce_energy(ENERGY_COSTS["fish"])
            print(f"Deducted {ENERGY_COSTS['fish']} energy. Current energy: {self.player.get_energy()}")

    def catch_fish(self):
        """Handle catching a fish and updating inventory."""
        fish_list = FISH_DAY if self.time_of_day == "Day" else FISH_NIGHT
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

        print(f"You caught a {self.caught_fish}!")

def start_fishing(player, time_of_day, screen):
    if player.get_energy() >= ENERGY_COSTS["fish"]:
        minigame = FishingMinigame(player, time_of_day, screen)
        minigame.run()
    else:
        print("Not enough energy to fish!")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player()
    player.energy = 100
    start_fishing(player, "day", screen)
    pygame.quit()