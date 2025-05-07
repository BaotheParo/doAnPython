import pygame
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

from src.core.game_state import GameState
from src.core.ui import SettingsUI
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.core.sound_manager import SoundManager

class VillageScene:
    def __init__(self, game_state, screen, ui):
        self.game_state = game_state
        self.screen = screen
        self.ui = ui
        pygame.display.set_caption("Village Area")

        # Initialize SoundManager if not present
        if not hasattr(self.game_state, 'sound_manager'):
            self.game_state.sound_manager = SoundManager()

        self.ui.show_map = False

        # Fonts
        self.notification_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.tooltip_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.message_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 24, bold=True)

        self.notification_text = "Moved to the village"
        self.notification_surface = self.notification_font.render(self.notification_text, True, WHITE)
        self.notification_timer = 3000
        self.notification_start_time = pygame.time.get_ticks()
        self.notification_alpha = 200

        self.day_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-ngoilang.png")
        self.night_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-ngoilang-dem.png")

        try:
            self.day_background = pygame.image.load(self.day_background_path).convert()
            self.day_background = pygame.transform.scale(self.day_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_background = pygame.image.load(self.night_background_path).convert()
            self.night_background = pygame.transform.scale(self.night_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            self.day_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.day_background.fill((100, 200, 100))
            self.night_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_background.fill((0, 0, 50))

        self.farmer_trader_rect = pygame.Rect(47, 271, 130, 325)
        self.fisher_trader_rect = pygame.Rect(562, 265, 100, 280)

        self.tooltips = {
            "farmer_trader": self.tooltip_font.render("Farmer Trader", True, WHITE),
            "fisher_trader": self.tooltip_font.render("Fisher Trader", True, WHITE),
            "buy_seed": self.tooltip_font.render("Sell Crops", True, WHITE),
            "sell_crop": self.tooltip_font.render("Buy Seeds", True, WHITE),
            "buy_farm": self.tooltip_font.render("Buy Land", True, WHITE),
            "sell_fish": self.tooltip_font.render("Sell Fish", True, WHITE),
            "buy_rod": self.tooltip_font.render("Buy Fishing Rod", True, WHITE),
            "carrot_seed": self.tooltip_font.render("Carrot Seed - 2 coins", True, WHITE),
            "cabbage_seed": self.tooltip_font.render("Cabbage Seed - 3 coins", True, WHITE),
            "beetroot_seed": self.tooltip_font.render("Beetroot Seed - 5 coins", True, WHITE),
            "pumpkin_seed": self.tooltip_font.render("Pumpkin Seed - 6 coins", True, WHITE),
            "rare_herb_seed": self.tooltip_font.render("Rare Herb Seed - 5 frogs", True, WHITE),
            "energy_herb_seed": self.tooltip_font.render("Energy Herb Seed - 3 frogs", True, WHITE),
            "carrot_crop": self.tooltip_font.render("Carrot - 3 coins", True, WHITE),
            "cabbage_crop": self.tooltip_font.render("Cabbage - 4 coins", True, WHITE),
            "beetroot_crop": self.tooltip_font.render("Beetroot - 7 coins", True, WHITE),
            "pumpkin_crop": self.tooltip_font.render("Pumpkin - 9 coins", True, WHITE),
            "rare_herb": self.tooltip_font.render("Rare Herb - 15 coins", True, WHITE),
            "energy_herb": self.tooltip_font.render("Energy Herb - 10 coins", True, WHITE),
            "tilapia": self.tooltip_font.render("Tilapia - 5 coins", True, WHITE),
            "carp": self.tooltip_font.render("Carp - 7 coins", True, WHITE),
            "catfish": self.tooltip_font.render("Catfish - 10 coins", True, WHITE),
            "eel": self.tooltip_font.render("Eel - 15 coins", True, WHITE),
            "ghost_fish": self.tooltip_font.render("Ghost Fish - 20 coins", True, WHITE),
            "silver_rod": self.tooltip_font.render("Silver Rod - 20 coins", True, WHITE),
            "gold_rod": self.tooltip_font.render("Gold Rod - 50 coins", True, WHITE),
            "platinum_rod": self.tooltip_font.render("Platinum Rod - 100 coins", True, WHITE),
            "expand_2_to_4": self.tooltip_font.render("Expand 2 to 4 slots - 18 coins", True, WHITE),
            "expand_4_to_6": self.tooltip_font.render("Expand 4 to 6 slots - 25 coins", True, WHITE),
            "expand_6_to_8": self.tooltip_font.render("Expand 6 to 8 slots - 32 coins", True, WHITE),
            "exit_menu": self.tooltip_font.render("Exit", True, WHITE),
        }

        self.menu_images = {
            "menubanhat": os.path.join(BASE_DIR, "assets", "images", "fish", "menubanhat.png"),
            "menubanrau": os.path.join(BASE_DIR, "assets", "images", "fish", "menubanrau.png"),
            "menumuadat": os.path.join(BASE_DIR, "assets", "images", "fish", "menumuadat.png"),
            "menubanca": os.path.join(BASE_DIR, "assets", "images", "fish", "menubanca.png"),
            "menucancau": os.path.join(BASE_DIR, "assets", "images", "fish", "menucancau.png")
        }
        self.current_menu = "menubanhat"

        try:
            self.menu_image = pygame.image.load(self.menu_images[self.current_menu]).convert_alpha()
            self.menu_image = pygame.transform.scale(self.menu_image, (387, 539))
        except FileNotFoundError:
            print(f"Error: File not found {self.menu_images[self.current_menu]}")
            self.menu_image = pygame.Surface((387, 539))
            self.menu_image.fill((255, 0, 0))

        self.menu_x = (SCREEN_WIDTH - self.menu_image.get_width()) // 2
        self.menu_y = (SCREEN_HEIGHT - self.menu_image.get_height()) // 2
        self.menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_image.get_width(), self.menu_image.get_height())

        self.buy_seed_rect = pygame.Rect(500, 109, 95, 65)
        self.sell_crop_rect = pygame.Rect(651, 109, 95, 65)
        self.buy_farm_rect = pygame.Rect(754, 204, 50, 90)
        self.sell_fish_rect = pygame.Rect(500, 109, 95, 65)
        self.buy_rod_rect = pygame.Rect(651, 109, 95, 65)

        self.cabbage_seed_rect = pygame.Rect(490, 249, 93, 80)
        self.pumpkin_seed_rect = pygame.Rect(577, 249, 93, 80)
        self.carrot_seed_rect = pygame.Rect(665, 249, 93, 80)
        self.beetroot_seed_rect = pygame.Rect(490, 357, 93, 80)
        self.rare_herb_seed_rect = pygame.Rect(577, 357, 93, 80)
        self.energy_herb_seed_rect = pygame.Rect(665, 357, 93, 80)

        self.cabbage_crop_rect = pygame.Rect(490, 249, 93, 80)
        self.pumpkin_crop_rect = pygame.Rect(577, 249, 93, 80)
        self.carrot_crop_rect = pygame.Rect(665, 249, 93, 80)
        self.beetroot_crop_rect = pygame.Rect(490, 357, 93, 80)
        self.rare_herb_rect = pygame.Rect(577, 357, 93, 80)
        self.energy_herb_rect = pygame.Rect(665, 357, 93, 80)

        self.carophi_rect = pygame.Rect(490, 249, 93, 80)
        self.cachep_rect = pygame.Rect(577, 249, 93, 80)
        self.catre_rect = pygame.Rect(665, 249, 93, 80)
        self.cachinh_rect = pygame.Rect(490, 357, 93, 80)
        self.cama_rect = pygame.Rect(577, 357, 93, 80)

        self.silver_rod_rect = pygame.Rect(490, 249, 93, 80)
        self.gold_rod_rect = pygame.Rect(577, 249, 93, 80)
        self.platinum_rod_rect = pygame.Rect(665, 249, 93, 80)

        self.expand_2_to_4_rect = pygame.Rect(490, 249, 93, 80)
        self.expand_4_to_6_rect = pygame.Rect(577, 249, 93, 80)
        self.expand_6_to_8_rect = pygame.Rect(665, 249, 93, 80)

        self.exit_button_rect = pygame.Rect(690, 500, 60, 30)
        self.exit_button_text = self.button_font.render("Exit", True, WHITE)
        self.exit_button_hover = False

        self.back_button_rect = pygame.Rect(10, SCREEN_HEIGHT - 50, 150, 40)
        self.back_button_text = self.button_font.render("Back to Farm", True, WHITE)
        self.back_button_hover = False

        self.show_menu = False
        self.show_message = False
        self.message_text = self.message_font.render("Insufficient funds!", True, WHITE)
        self.ok_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 30, 100, 40)
        self.ok_button_text = self.button_font.render("OK", True, WHITE)
        self.ok_button_hover = False

        self.running = True

    def show_notification(self, message, success=True):
        self.show_message = True
        self.message_text = self.message_font.render(message, True, WHITE)
        self.message_bg_color = (50, 200, 50, 220) if success else (200, 50, 50, 220)
        message_w = max(400, self.message_text.get_width() + 20)
        message_h = 150
        self.message_bg = pygame.Surface((message_w, message_h), pygame.SRCALPHA)
        pygame.draw.rect(self.message_bg, self.message_bg_color, (0, 0, message_w, message_h), border_radius=10)
        pygame.draw.rect(self.message_bg, (255, 255, 255), (0, 0, message_w, message_h), 2, border_radius=10)
        if success:
            self.game_state.sound_manager.play_sound('complete')

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = clock.tick(60)
            self.game_state.time_system.update(delta_time, self.game_state.player)  

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not (self.ui.show_map or self.ui.show_inventory):
                        if self.show_message:
                            if self.ok_button_rect.collidepoint(mouse_pos):
                                self.show_message = False
                        else:
                            self.handle_click(mouse_pos)
                    self.ui.handle_event(event)
                    if self.back_button_rect.collidepoint(mouse_pos):
                        from src.scenes.farm import FarmScene
                        print("Switching to FarmScene!")
                        self.running = False
                        farm_scene = FarmScene(self.game_state, self.screen, self.ui)
                        farm_scene.run()

            if self.game_state.time_system.is_day():
                self.screen.blit(self.day_background, (0, 0))
            else:
                self.screen.blit(self.night_background, (0, 0))

            if self.show_menu:
                self.screen.blit(self.menu_image, (self.menu_x, self.menu_y))
                self.exit_button_hover = self.exit_button_rect.collidepoint(mouse_pos)
                exit_button_bg = pygame.Surface((60, 30), pygame.SRCALPHA)
                exit_color = (150, 150, 150) if self.exit_button_hover else (100, 100, 100)
                pygame.draw.rect(exit_button_bg, exit_color, (0, 0, 60, 30), border_radius=5)
                pygame.draw.rect(exit_button_bg, (255, 255, 255), (0, 0, 60, 30), 2, border_radius=5)
                self.screen.blit(exit_button_bg, (self.exit_button_rect.x, self.exit_button_rect.y))
                exit_text_rect = self.exit_button_text.get_rect(center=self.exit_button_rect.center)
                self.screen.blit(self.exit_button_text, exit_text_rect)

            if not self.show_menu and not self.show_message and not (self.ui.show_map or self.ui.show_inventory):
                for rect, name in [(self.farmer_trader_rect, "farmer_trader"), (self.fisher_trader_rect, "fisher_trader")]:
                    if rect.collidepoint(mouse_pos):
                        tooltip_text = self.tooltips[name]
                        tooltip_w = tooltip_text.get_width() + 16
                        tooltip_h = tooltip_text.get_height() + 16
                        tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                        pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                        pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                        tooltip_x = rect.x
                        tooltip_y = rect.y - tooltip_h - 5
                        if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                            tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                        if tooltip_y < 10:
                            tooltip_y = rect.y + rect.height + 5
                        self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                        self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

            if self.show_menu and not self.show_message and not (self.ui.show_map or self.ui.show_inventory):
                if self.exit_button_rect.collidepoint(mouse_pos):
                    tooltip_text = self.tooltips["exit_menu"]
                    tooltip_w = tooltip_text.get_width() + 16
                    tooltip_h = tooltip_text.get_height() + 16
                    tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                    pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                    pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                    tooltip_x = self.exit_button_rect.x
                    tooltip_y = self.exit_button_rect.y - tooltip_h - 5
                    if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                        tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                    if tooltip_y < 10:
                        tooltip_y = self.exit_button_rect.y + self.exit_button_rect.height + 5
                    self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                    self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

                if self.current_menu in ["menubanhat", "menubanrau", "menumuadat"]:
                    for rect, name in [(self.buy_seed_rect, "buy_seed"), (self.sell_crop_rect, "sell_crop"), (self.buy_farm_rect, "buy_farm")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_text = self.tooltips[name]
                            tooltip_w = tooltip_text.get_width() + 16
                            tooltip_h = tooltip_text.get_height() + 16
                            tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                            pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                            pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                            tooltip_x = rect.x
                            tooltip_y = rect.y - tooltip_h - 5
                            if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                                tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                            if tooltip_y < 10:
                                tooltip_y = rect.y + rect.height + 5
                            self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

                elif self.current_menu in ["menubanca", "menucancau"]:
                    for rect, name in [(self.sell_fish_rect, "sell_fish"), (self.buy_rod_rect, "buy_rod")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_text = self.tooltips[name]
                            tooltip_w = tooltip_text.get_width() + 16
                            tooltip_h = tooltip_text.get_height() + 16
                            tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                            pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                            pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                            tooltip_x = rect.x
                            tooltip_y = rect.y - tooltip_h - 5
                            if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                                tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                            if tooltip_y < 10:
                                tooltip_y = rect.y + rect.height + 5
                            self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

                if self.current_menu == "menubanhat":
                    for rect, name in [(self.cabbage_seed_rect, "cabbage_seed"), (self.pumpkin_seed_rect, "pumpkin_seed"),
                                       (self.carrot_seed_rect, "carrot_seed"), (self.beetroot_seed_rect, "beetroot_seed"),
                                       (self.rare_herb_seed_rect, "rare_herb_seed"), (self.energy_herb_seed_rect, "energy_herb_seed")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_text = self.tooltips[name]
                            tooltip_w = tooltip_text.get_width() + 16
                            tooltip_h = tooltip_text.get_height() + 16
                            tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                            pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                            pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                            tooltip_x = rect.x
                            tooltip_y = rect.y - tooltip_h - 5
                            if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                                tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                            if tooltip_y < 10:
                                tooltip_y = rect.y + rect.height + 5
                            self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

                if self.current_menu == "menubanrau":
                    for rect, name in [(self.cabbage_crop_rect, "cabbage_crop"), (self.pumpkin_crop_rect, "pumpkin_crop"),
                                       (self.carrot_crop_rect, "carrot_crop"), (self.beetroot_crop_rect, "beetroot_crop"),
                                       (self.rare_herb_rect, "rare_herb"), (self.energy_herb_rect, "energy_herb")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_text = self.tooltips[name]
                            tooltip_w = tooltip_text.get_width() + 16
                            tooltip_h = tooltip_text.get_height() + 16
                            tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                            pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                            pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                            tooltip_x = rect.x
                            tooltip_y = rect.y - tooltip_h - 5
                            if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                                tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                            if tooltip_y < 10:
                                tooltip_y = rect.y + rect.height + 5
                            self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

                if self.current_menu == "menubanca":
                    for rect, name in [(self.carophi_rect, "tilapia"), (self.cachep_rect, "carp"),
                                       (self.catre_rect, "catfish"), (self.cachinh_rect, "eel"), (self.cama_rect, "ghost_fish")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_text = self.tooltips[name]
                            tooltip_w = tooltip_text.get_width() + 16
                            tooltip_h = tooltip_text.get_height() + 16
                            tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                            pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                            pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                            tooltip_x = rect.x
                            tooltip_y = rect.y - tooltip_h - 5
                            if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                                tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                            if tooltip_y < 10:
                                tooltip_y = rect.y + rect.height + 5
                            self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

                if self.current_menu == "menucancau":
                    for rect, name in [(self.silver_rod_rect, "silver_rod"), (self.gold_rod_rect, "gold_rod"),
                                       (self.platinum_rod_rect, "platinum_rod")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_text = self.tooltips[name]
                            tooltip_w = tooltip_text.get_width() + 16
                            tooltip_h = tooltip_text.get_height() + 16
                            tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                            pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                            pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                            tooltip_x = rect.x
                            tooltip_y = rect.y - tooltip_h - 5
                            if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                                tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                            if tooltip_y < 10:
                                tooltip_y = rect.y + rect.height + 5
                            self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

                if self.current_menu == "menumuadat":
                    for rect, name in [(self.expand_2_to_4_rect, "expand_2_to_4"), (self.expand_4_to_6_rect, "expand_4_to_6"),
                                       (self.expand_6_to_8_rect, "expand_6_to_8")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_text = self.tooltips[name]
                            tooltip_w = tooltip_text.get_width() + 16
                            tooltip_h = tooltip_text.get_height() + 16
                            tooltip_bg = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
                            pygame.draw.rect(tooltip_bg, (50, 50, 50, 220), (0, 0, tooltip_w, tooltip_h), border_radius=5)
                            pygame.draw.rect(tooltip_bg, (255, 255, 255), (0, 0, tooltip_w, tooltip_h), 2, border_radius=5)
                            tooltip_x = rect.x
                            tooltip_y = rect.y - tooltip_h - 5
                            if tooltip_x + tooltip_w > SCREEN_WIDTH - 10:
                                tooltip_x = SCREEN_WIDTH - tooltip_w - 10
                            if tooltip_y < 10:
                                tooltip_y = rect.y + rect.height + 5
                            self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(tooltip_text, (tooltip_x + 8, tooltip_y + 8))

            if self.show_message:
                message_w = max(400, self.message_text.get_width() + 20)
                message_x = SCREEN_WIDTH // 2 - message_w // 2
                message_y = SCREEN_HEIGHT // 2 - 150 // 2
                self.screen.blit(self.message_bg, (message_x, message_y))
                text_rect = self.message_text.get_rect(center=(message_x + message_w // 2, message_y + 50))
                self.screen.blit(self.message_text, text_rect)
                self.ok_button_hover = self.ok_button_rect.collidepoint(mouse_pos)
                ok_button_bg = pygame.Surface((100, 40), pygame.SRCALPHA)
                ok_color = (150, 150, 150) if self.ok_button_hover else (100, 100, 100)
                pygame.draw.rect(ok_button_bg, ok_color, (0, 0, 100, 40), border_radius=5)
                pygame.draw.rect(ok_button_bg, (255, 255, 255), (0, 0, 100, 40), 2, border_radius=5)
                self.screen.blit(ok_button_bg, (self.ok_button_rect.x, self.ok_button_rect.y))
                ok_text_rect = self.ok_button_text.get_rect(center=self.ok_button_rect.center)
                self.screen.blit(self.ok_button_text, ok_text_rect)

            if self.notification_timer > 0:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.notification_start_time
                if elapsed_time < self.notification_timer:
                    alpha = max(0, self.notification_alpha * (1 - elapsed_time / self.notification_timer))
                    text_rect = self.notification_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
                    bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
                    pygame.draw.rect(bg_surface, (0, 0, 0, int(alpha)), (0, 0, text_rect.width + 20, text_rect.height + 10), border_radius=5)
                    pygame.draw.rect(bg_surface, (255, 255, 255, int(alpha)), (0, 0, text_rect.width + 20, text_rect.height + 10), 2, border_radius=5)
                    self.screen.blit(bg_surface, (text_rect.x - 10, text_rect.y - 5))
                    notification_surface = self.notification_surface.copy()
                    notification_surface.set_alpha(int(alpha))
                    self.screen.blit(notification_surface, text_rect)
                else:
                    self.notification_timer = 0

            self.back_button_hover = self.back_button_rect.collidepoint(mouse_pos)
            back_button_bg = pygame.Surface((150, 40), pygame.SRCALPHA)
            back_color = (80, 80, 80, 220) if self.back_button_hover else (50, 50, 50, 220)
            pygame.draw.rect(back_button_bg, back_color, (0, 0, 150, 40), border_radius=5)
            pygame.draw.rect(back_button_bg, (255, 255, 255), (0, 0, 150, 40), 2, border_radius=5)
            self.screen.blit(back_button_bg, (self.back_button_rect.x, self.back_button_rect.y))
            back_text_rect = self.back_button_text.get_rect(center=self.back_button_rect.center)
            self.screen.blit(self.back_button_text, back_text_rect)

            # Remove mouse position display for cleaner UI
            money_text = self.button_font.render(f"Money: {self.game_state.player.money}", True, WHITE)
            money_bg = pygame.Surface((150, 25), pygame.SRCALPHA)
            pygame.draw.rect(money_bg, (50, 50, 50, 220), (0, 0, 150, 25), border_radius=5)
            self.screen.blit(money_bg, (10, 10))
            self.screen.blit(money_text, (15, 15))

            time_text = self.button_font.render(
                f"Day: {self.game_state.time_system.current_day} | {self.game_state.time_system.get_time_of_day()} | Time Left: {self.game_state.time_system.format_time(self.game_state.time_system.get_remaining_time())}",
                True, WHITE
            )
            time_bg = pygame.Surface((300, 25), pygame.SRCALPHA)
            pygame.draw.rect(time_bg, (50, 50, 50, 220), (0, 0, 300, 25), border_radius=5)
            self.screen.blit(time_bg, (10, 40))
            self.screen.blit(time_text, (15, 45))

            self.ui.draw()
            pygame.display.flip()

    def handle_click(self, pos):
        if not self.show_menu and self.farmer_trader_rect.collidepoint(pos):
            self.game_state.sound_manager.play_sound('click')
            self.show_menu = True
            self.current_menu = "menubanhat"
            self.update_menu_image()

        elif not self.show_menu and self.fisher_trader_rect.collidepoint(pos):
            self.game_state.sound_manager.play_sound('click')
            self.show_menu = True
            self.current_menu = "menubanca"
            self.update_menu_image()

        elif self.show_menu:
            if self.exit_button_rect.collidepoint(pos):
                self.show_menu = False
                print("Menu closed!")
                return

            if self.current_menu in ["menubanhat", "menubanrau", "menumuadat"]:
                if self.buy_seed_rect.collidepoint(pos):
                    print("Sell crops")
                    self.current_menu = "menubanrau"
                    self.update_menu_image()
                elif self.sell_crop_rect.collidepoint(pos):
                    print("Buy seeds")
                    self.current_menu = "menubanhat"
                    self.update_menu_image()
                elif self.buy_farm_rect.collidepoint(pos):
                    print("Buy land")
                    self.current_menu = "menumuadat"
                    self.update_menu_image()

            elif self.current_menu in ["menubanca", "menucancau"]:
                if self.sell_fish_rect.collidepoint(pos):
                    print("Sell fish")
                    self.current_menu = "menubanca"
                    self.update_menu_image()
                elif self.buy_rod_rect.collidepoint(pos):
                    print("Buy fishing rod")
                    self.current_menu = "menucancau"
                    self.update_menu_image()

            if self.current_menu == "menubanhat":
                if self.cabbage_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(3):
                        self.game_state.player.inventory.add_item("cabbage_seed", 1)
                        self.show_notification("Purchased Cabbage Seed - 3 coins!", success=True)
                    else:
                        self.show_notification("Insufficient funds!", success=False)
                elif self.pumpkin_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(6):
                        self.game_state.player.inventory.add_item("pumpkin_seed", 1)
                        self.show_notification("Purchased Pumpkin Seed - 6 coins!", success=True)
                    else:
                        self.show_notification("Insufficient funds!", success=False)
                elif self.carrot_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(2):
                        self.game_state.player.inventory.add_item("carrot_seed", 1)
                        self.show_notification("Purchased Carrot Seed - 2 coins!", success=True)
                    else:
                        self.show_notification("Insufficient funds!", success=False)
                elif self.beetroot_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(5):
                        self.game_state.player.inventory.add_item("beetroot_seed", 1)
                        self.show_notification("Purchased Beetroot Seed - 5 coins!", success=True)
                    else:
                        self.show_notification("Insufficient funds!", success=False)
                elif self.rare_herb_seed_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("frog", 5):
                        self.game_state.player.inventory.remove_item("frog", 5)
                        self.game_state.player.inventory.add_item("rare_herb_seed", 1)
                        self.show_notification("Purchased Rare Herb Seed - 5 frogs!", success=True)
                    else:
                        self.show_notification("Not enough frogs!", success=False)
                elif self.energy_herb_seed_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("frog", 3):
                        self.game_state.player.inventory.remove_item("frog", 3)
                        self.game_state.player.inventory.add_item("energy_herb_seed", 1)
                        self.show_notification("Purchased Energy Herb Seed - 3 frogs!", success=True)
                    else:
                        self.show_notification("Not enough frogs!", success=False)

            elif self.current_menu == "menubanrau":
                if self.cabbage_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("cabbage", 1):
                        self.game_state.player.inventory.remove_item("cabbage", 1)
                        self.game_state.player.add_money(4)
                        self.show_notification("Sold Cabbage, received 4 coins!", success=True)
                    else:
                        self.show_notification("No Cabbage to sell!", success=False)
                elif self.pumpkin_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("pumpkin", 1):
                        self.game_state.player.inventory.remove_item("pumpkin", 1)
                        self.game_state.player.add_money(9)
                        self.show_notification("Sold Pumpkin, received 9 coins!", success=True)
                    else:
                        self.show_notification("No Pumpkin to sell!", success=False)
                elif self.carrot_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("carrot", 1):
                        self.game_state.player.inventory.remove_item("carrot", 1)
                        self.game_state.player.add_money(3)
                        self.show_notification("Sold Carrot, received 3 coins!", success=True)
                    else:
                        self.show_notification("No Carrot to sell!", success=False)
                elif self.beetroot_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("beetroot", 1):
                        self.game_state.player.inventory.remove_item("beetroot", 1)
                        self.game_state.player.add_money(7)
                        self.show_notification("Sold Beetroot, received 7 coins!", success=True)
                    else:
                        self.show_notification("No Beetroot to sell!", success=False)
                elif self.rare_herb_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("rare_herb", 1):
                        self.game_state.player.inventory.remove_item("rare_herb", 1)
                        self.game_state.player.add_money(15)
                        self.show_notification("Sold Rare Herb, received 15 coins!", success=True)
                    else:
                        self.show_notification("No Rare Herb to sell!", success=False)
                elif self.energy_herb_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("energy_herb", 1):
                        self.game_state.player.inventory.remove_item("energy_herb", 1)
                        self.game_state.player.add_money(10)
                        self.show_notification("Sold Energy Herb, received 10 coins!", success=True)
                    else:
                        self.show_notification("No Energy Herb to sell!", success=False)

            elif self.current_menu == "menubanca":
                if self.carophi_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("tilapia", 1):
                        self.game_state.player.inventory.remove_item("tilapia", 1)
                        self.game_state.player.add_money(5)
                        self.show_notification("Sold Tilapia, received 5 coins!", success=True)
                    else:
                        self.show_notification("No Tilapia to sell!", success=False)
                elif self.cachep_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("carp", 1):
                        self.game_state.player.inventory.remove_item("carp", 1)
                        self.game_state.player.add_money(7)
                        self.show_notification("Sold Carp, received 7 coins!", success=True)
                    else:
                        self.show_notification("No Carp to sell!", success=False)
                elif self.catre_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("catfish", 1):
                        self.game_state.player.inventory.remove_item("catfish", 1)
                        self.game_state.player.add_money(10)
                        self.show_notification("Sold Catfish, received 10 coins!", success=True)
                    else:
                        self.show_notification("No Catfish to sell!", success=False)
                elif self.cachinh_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("eel", 1):
                        self.game_state.player.inventory.remove_item("eel", 1)
                        self.game_state.player.add_money(15)
                        self.show_notification("Sold Eel, received 15 coins!", success=True)
                    else:
                        self.show_notification("No Eel to sell!", success=False)
                elif self.cama_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("ghost_fish", 1):
                        self.game_state.player.inventory.remove_item("ghost_fish", 1)
                        self.game_state.player.add_money(20)
                        self.show_notification("Sold Ghost Fish, received 20 coins!", success=True)
                    else:
                        self.show_notification("No Ghost Fish to sell!", success=False)

            elif self.current_menu == "menucancau":
                if self.silver_rod_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(20):
                        self.game_state.player.upgrade_rod("silver")
                        self.show_notification("Purchased Silver Rod - 20 coins!", success=True)
                    else:
                        self.show_notification("Insufficient funds!", success=False)
                elif self.gold_rod_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(50):
                        self.game_state.player.upgrade_rod("gold")
                        self.show_notification("Purchased Gold Rod - 50 coins!", success=True)
                    else:
                        self.show_notification("Insufficient funds!", success=False)
                elif self.platinum_rod_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(100):
                        self.game_state.player.upgrade_rod("diamond")
                        self.show_notification("Purchased Platinum Rod - 100 coins!", success=True)
                    else:
                        self.show_notification("Insufficient funds!", success=False)

            elif self.current_menu == "menumuadat":
                current_garden_slots = self.game_state.player.garden_slots

                if self.expand_2_to_4_rect.collidepoint(pos):
                    if current_garden_slots >= 4:
                        self.show_notification("You already have 4 slots!", success=False)
                    elif current_garden_slots != 2:
                        self.show_notification("You need 2 slots to expand to 4!", success=False)
                    else:
                        if self.game_state.player.upgrade_garden(4):
                            self.show_notification("Expanded garden to 4 slots - 18 coins!", success=True)
                        else:
                            self.show_notification("Insufficient funds!", success=False)

                elif self.expand_4_to_6_rect.collidepoint(pos):
                    if current_garden_slots >= 6:
                        self.show_notification("You already have 6 slots!", success=False)
                    elif current_garden_slots != 4:
                        self.show_notification("You need to expand to 4 slots first!", success=False)
                    else:
                        if self.game_state.player.upgrade_garden(6):
                            self.show_notification("Expanded garden to 6 slots - 25 coins!", success=True)
                        else:
                            self.show_notification("Insufficient funds!", success=False)

                elif self.expand_6_to_8_rect.collidepoint(pos):
                    if current_garden_slots >= 8:
                        self.show_notification("You already have 8 slots!", success=False)
                    elif current_garden_slots != 6:
                        self.show_notification("You need to expand to 6 slots first!", success=False)
                    else:
                        if self.game_state.player.upgrade_garden(8):
                            self.show_notification("Expanded garden to 8 slots - 32 coins!", success=True)
                        else:
                            self.show_notification("Insufficient funds!", success=False)

            elif not self.menu_rect.collidepoint(pos):
                self.show_menu = False
                print("Menu closed!")

    def update_menu_image(self):
        try:
            self.menu_image = pygame.image.load(self.menu_images[self.current_menu]).convert_alpha()
            self.menu_image = pygame.transform.scale(self.menu_image, (387, 539))
        except FileNotFoundError:
            print(f"Error: File not found {self.menu_images[self.current_menu]}")
            self.menu_image = pygame.Surface((387, 539))
            self.menu_image.fill((255, 0, 0))

        self.menu_x = (SCREEN_WIDTH - self.menu_image.get_width()) // 2
        self.menu_y = (SCREEN_HEIGHT - self.menu_image.get_height()) // 2
        self.menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_image.get_width(), self.menu_image.get_height())

        self.buy_seed_rect = pygame.Rect(500, 109, 95, 65)
        self.sell_crop_rect = pygame.Rect(651, 109, 95, 65)
        self.buy_farm_rect = pygame.Rect(754, 204, 50, 90)
        self.sell_fish_rect = pygame.Rect(500, 109, 95, 65)
        self.buy_rod_rect = pygame.Rect(651, 109, 95, 65)