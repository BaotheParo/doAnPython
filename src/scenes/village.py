import pygame
import os
import sys

# Thêm đường dẫn gốc của dự án vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# Lấy đường dẫn tuyệt đối đến thư mục gốc của dự án
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

from src.core.game_state import GameState
from src.core.ui import SettingsUI
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class VillageScene:
    def __init__(self, game_state, screen, ui):
        self.game_state = game_state
        self.screen = screen
        self.ui = ui
        pygame.display.set_caption("Khu vực làng")

        # Tắt bản đồ ngay khi vào VillageScene
        self.ui.show_map = False  # Đảm bảo bản đồ không hiển thị khi chuyển đến khu vực làng

        # Đường dẫn tuyệt đối đến các file background
        self.day_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-ngoilang.png")
        self.night_background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "background-ngoilang-dem.png")

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
        self.farmer_trader_rect = pygame.Rect(47, 271, 130, 325)  # Thương nhân nông trại
        self.fisher_trader_rect = pygame.Rect(562, 265, 100, 280)  # Thương nhân câu cá

        # Tooltip cho các khu vực tương tác, các ô trong menu, các loại nông sản, và các tùy chọn mua đất
        self.tooltip_font = pygame.font.SysFont(None, 25)
        self.tooltips = {
            "farmer_trader": self.tooltip_font.render("Thương nhân nông trại", True, WHITE),
            "fisher_trader": self.tooltip_font.render("Thương nhân câu cá", True, WHITE),
            "buy_seed": self.tooltip_font.render("Bán nông sản", True, WHITE),
            "sell_crop": self.tooltip_font.render("Mua hạt giống", True, WHITE),
            "buy_farm": self.tooltip_font.render("Mua đất", True, WHITE),
            "sell_fish": self.tooltip_font.render("Bán cá", True, WHITE),
            "buy_rod": self.tooltip_font.render("Mua cần câu", True, WHITE),
            "carrot_seed": self.tooltip_font.render("Hạt cà rốt - 2 đồng", True, WHITE),
            "cabbage_seed": self.tooltip_font.render("Hạt bắp cải - 3 đồng", True, WHITE),
            "beetroot_seed": self.tooltip_font.render("Hạt củ dền - 5 đồng", True, WHITE),
            "pumpkin_seed": self.tooltip_font.render("Hạt bí đỏ - 6 đồng", True, WHITE),
            "rare_herb_seed": self.tooltip_font.render("Hạt thảo mộc hiếm - 5 ếch", True, WHITE),
            "energy_herb_seed": self.tooltip_font.render("Hạt thảo mộc năng lượng - 3 ếch", True, WHITE),
            "carrot_crop": self.tooltip_font.render("Cà rốt - 3 đồng", True, WHITE),
            "cabbage_crop": self.tooltip_font.render("Bắp cải - 4 đồng", True, WHITE),
            "beetroot_crop": self.tooltip_font.render("Củ dền - 7 đồng", True, WHITE),
            "pumpkin_crop": self.tooltip_font.render("Bí đỏ - 9 đồng", True, WHITE),
            "rare_herb": self.tooltip_font.render("Thảo mộc hiếm - 15 đồng", True, WHITE),
            "energy_herb": self.tooltip_font.render("Thảo mộc năng lượng - 10 đồng", True, WHITE),
            "tilapia": self.tooltip_font.render("Cá rô phi - 5 đồng", True, WHITE),
            "carp": self.tooltip_font.render("Cá chép - 7 đồng", True, WHITE),
            "catfish": self.tooltip_font.render("Cá trê - 10 đồng", True, WHITE),
            "eel": self.tooltip_font.render("Cá chình - 15 đồng", True, WHITE),
            "ghost_fish": self.tooltip_font.render("Cá ma - 20 đồng", True, WHITE),
            "silver_rod": self.tooltip_font.render("Cần câu bạc - 20 đồng", True, WHITE),
            "gold_rod": self.tooltip_font.render("Cần câu vàng - 50 đồng", True, WHITE),
            "platinum_rod": self.tooltip_font.render("Cần câu bạch kim - 100 đồng", True, WHITE),
            "expand_2_to_4": self.tooltip_font.render("Mở rộng 2 ô -> 4 ô - 18 đồng", True, WHITE),
            "expand_4_to_6": self.tooltip_font.render("Mở rộng 4 ô -> 6 ô - 25 đồng", True, WHITE),
            "expand_6_to_8": self.tooltip_font.render("Mở rộng 6 ô -> 8 ô - 32 đồng", True, WHITE),
            "exit_menu": self.tooltip_font.render("Thoát", True, WHITE),
        }
        self.tooltip_bg = pygame.Surface((200, 35))
        self.tooltip_bg.fill((50, 50, 50))

        # Font để hiển thị tọa độ chuột và thời gian
        self.mouse_pos_font = pygame.font.SysFont(None, 25)

        # Tải các hình ảnh menu (đường dẫn tuyệt đối)
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
            print(f"Lỗi: Không tìm thấy file {self.menu_images[self.current_menu]}")
            self.menu_image = pygame.Surface((387, 539))
            self.menu_image.fill((255, 0, 0))

        # Tính toán vị trí để menu nằm giữa màn hình
        self.menu_x = (SCREEN_WIDTH - self.menu_image.get_width()) // 2
        self.menu_y = (SCREEN_HEIGHT - self.menu_image.get_height()) // 2

        # Định nghĩa khu vực của menu
        self.menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_image.get_width(), self.menu_image.get_height())

        # Định nghĩa các ô vuông trên menu (tọa độ tuyệt đối)
        # Menu nông trại
        self.buy_seed_rect = pygame.Rect(500, 109, 95, 65)
        self.sell_crop_rect = pygame.Rect(651, 109, 95, 65)
        self.buy_farm_rect = pygame.Rect(754, 204, 50, 90)
        # Menu câu cá
        self.sell_fish_rect = pygame.Rect(500, 109, 95, 65)
        self.buy_rod_rect = pygame.Rect(651, 109, 95, 65)

        # Định nghĩa các ô vuông cho các loại hạt giống (hiển thị khi ở menubanhat)
        self.cabbage_seed_rect = pygame.Rect(490, 249, 93, 80)  # Bắp cải
        self.pumpkin_seed_rect = pygame.Rect(577, 249, 93, 80)  # Bí đỏ
        self.carrot_seed_rect = pygame.Rect(665, 249, 93, 80)   # Cà rốt
        self.beetroot_seed_rect = pygame.Rect(490, 357, 93, 80) # Củ dền
        self.rare_herb_seed_rect = pygame.Rect(577, 357, 93, 80)  # Hạt thảo mộc hiếm
        self.energy_herb_seed_rect = pygame.Rect(665, 357, 93, 80)  # Hạt thảo mộc năng lượng

        # Định nghĩa các ô vuông cho các loại nông sản (hiển thị khi ở menubanrau)
        self.cabbage_crop_rect = pygame.Rect(490, 249, 93, 80)  # Bắp cải
        self.pumpkin_crop_rect = pygame.Rect(577, 249, 93, 80)  # Bí đỏ
        self.carrot_crop_rect = pygame.Rect(665, 249, 93, 80)   # Cà rốt
        self.beetroot_crop_rect = pygame.Rect(490, 357, 93, 80) # Củ dền
        self.rare_herb_rect = pygame.Rect(577, 357, 93, 80)     # Thảo dược hiếm
        self.energy_herb_rect = pygame.Rect(665, 357, 93, 80)   # Thảo mộc năng lượng

        # Định nghĩa các ô vuông cho các loại cá (hiển thị khi ở menubanca)
        self.carophi_rect = pygame.Rect(490, 249, 93, 80)
        self.cachep_rect = pygame.Rect(577, 249, 93, 80)
        self.catre_rect = pygame.Rect(665, 249, 93, 80)
        self.cachinh_rect = pygame.Rect(490, 357, 93, 80)
        self.cama_rect = pygame.Rect(577, 357, 93, 80)

        # Định nghĩa các ô vuông cho các loại cần câu (hiển thị khi ở menucancau)
        self.silver_rod_rect = pygame.Rect(490, 249, 93, 80)
        self.gold_rod_rect = pygame.Rect(577, 249, 93, 80)
        self.platinum_rod_rect = pygame.Rect(665, 249, 93, 80)

        # Định nghĩa các ô vuông cho các tùy chọn mua đất (hiển thị khi ở menumuadat)
        self.expand_2_to_4_rect = pygame.Rect(490, 249, 93, 80)
        self.expand_4_to_6_rect = pygame.Rect(577, 249, 93, 80)
        self.expand_6_to_8_rect = pygame.Rect(665, 249, 93, 80)

        # Định nghĩa nút "Thoát" trên menu
        self.exit_button_rect = pygame.Rect(690, 500, 60, 30)  # Góc dưới bên phải của menu
        self.exit_button_text = self.tooltip_font.render("Thoát", True, WHITE)
        self.exit_button_bg = pygame.Surface((60, 30))
        self.exit_button_bg.fill((100, 100, 100))

        # Nút "Back to Farm"
        self.back_button_rect = pygame.Rect(10, SCREEN_HEIGHT - 50, 150, 40)
        self.back_button_text = self.tooltip_font.render("Back to Farm", True, WHITE)
        self.back_button_bg = pygame.Surface((150, 40))
        self.back_button_bg.fill((50, 50, 50))
        self.back_button_hover = False

        # Biến để kiểm soát việc hiển thị menu
        self.show_menu = False

        # Biến để kiểm soát việc hiển thị thông báo
        self.show_message = False
        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
        self.message_bg = pygame.Surface((200, 100))
        self.message_bg.fill((50, 50, 50))
        self.ok_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 + 20, 60, 30)
        self.ok_button_text = self.tooltip_font.render("OK", True, WHITE)
        self.ok_button_bg = pygame.Surface((60, 30))
        self.ok_button_bg.fill((100, 100, 100))

        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = clock.tick(60)  # Thời gian trôi qua giữa các khung hình (ms)
            self.game_state.time_system.update(delta_time)  # Cập nhật thời gian trong game

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not (self.ui.show_map or self.ui.show_inventory):  # Không xử lý click nếu đang hiển thị map hoặc inventory
                        if self.show_message:
                            if self.ok_button_rect.collidepoint(mouse_pos):
                                self.show_message = False
                        else:
                            self.handle_click(mouse_pos)
                    self.ui.handle_event(event)  # Xử lý sự kiện cho UI
                    if self.back_button_rect.collidepoint(mouse_pos):
                        from src.scenes.farm import FarmScene
                        print("Chuyển về FarmScene!")
                        self.running = False
                        farm_scene = FarmScene(self.game_state, self.screen, self.ui)
                        farm_scene.run()

            # Vẽ background dựa trên thời gian
            if self.game_state.time_system.is_day():
                self.screen.blit(self.day_background, (0, 0))
            else:
                self.screen.blit(self.night_background, (0, 0))

            # Vẽ menu nếu đang hiển thị
            if self.show_menu:
                self.screen.blit(self.menu_image, (self.menu_x, self.menu_y))
                # Vẽ nút "Thoát" trên menu
                self.screen.blit(self.exit_button_bg, (self.exit_button_rect.x, self.exit_button_rect.y))
                self.screen.blit(self.exit_button_text, (self.exit_button_rect.x + 5, self.exit_button_rect.y + 5))

            # Hiển thị tooltip cho các khu vực tương tác
            if not self.show_menu and not self.show_message and not (self.ui.show_map or self.ui.show_inventory):
                for rect, name in [(self.farmer_trader_rect, "farmer_trader"),
                                   (self.fisher_trader_rect, "fisher_trader")]:
                    if rect.collidepoint(mouse_pos):
                        tooltip_x = rect.x
                        tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                        self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                        self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

            # Hiển thị tooltip cho các ô vuông trong menu
            if self.show_menu and not self.show_message and not (self.ui.show_map or self.ui.show_inventory):
                # Tooltip cho nút "Thoát"
                if self.exit_button_rect.collidepoint(mouse_pos):
                    tooltip_x = self.exit_button_rect.x
                    tooltip_y = self.exit_button_rect.y - self.tooltip_bg.get_height() - 5
                    self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                    self.screen.blit(self.tooltips["exit_menu"], (tooltip_x + 5, tooltip_y + 5))

                if self.current_menu in ["menubanhat", "menubanrau", "menumuadat"]:
                    for rect, name in [(self.buy_seed_rect, "buy_seed"),
                                       (self.sell_crop_rect, "sell_crop"),
                                       (self.buy_farm_rect, "buy_farm")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))
                elif self.current_menu in ["menubanca", "menucancau"]:
                    for rect, name in [(self.sell_fish_rect, "sell_fish"),
                                       (self.buy_rod_rect, "buy_rod")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                if self.current_menu == "menubanhat":
                    for rect, name in [(self.cabbage_seed_rect, "cabbage_seed"),
                                       (self.pumpkin_seed_rect, "pumpkin_seed"),
                                       (self.carrot_seed_rect, "carrot_seed"),
                                       (self.beetroot_seed_rect, "beetroot_seed"),
                                       (self.rare_herb_seed_rect, "rare_herb_seed"),
                                       (self.energy_herb_seed_rect, "energy_herb_seed")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                if self.current_menu == "menubanrau":
                    for rect, name in [(self.cabbage_crop_rect, "cabbage_crop"),
                                       (self.pumpkin_crop_rect, "pumpkin_crop"),
                                       (self.carrot_crop_rect, "carrot_crop"),
                                       (self.beetroot_crop_rect, "beetroot_crop"),
                                       (self.rare_herb_rect, "rare_herb"),
                                       (self.energy_herb_rect, "energy_herb")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                if self.current_menu == "menubanca":
                    for rect, name in [(self.carophi_rect, "tilapia"),
                                       (self.cachep_rect, "carp"),
                                       (self.catre_rect, "catfish"),
                                       (self.cachinh_rect, "eel"),
                                       (self.cama_rect, "ghost_fish")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                if self.current_menu == "menucancau":
                    for rect, name in [(self.silver_rod_rect, "silver_rod"),
                                       (self.gold_rod_rect, "gold_rod"),
                                       (self.platinum_rod_rect, "platinum_rod")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                if self.current_menu == "menumuadat":
                    for rect, name in [(self.expand_2_to_4_rect, "expand_2_to_4"),
                                       (self.expand_4_to_6_rect, "expand_4_to_6"),
                                       (self.expand_6_to_8_rect, "expand_6_to_8")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

            # Hiển thị thông báo nếu có
            if self.show_message:
                message_x = SCREEN_WIDTH // 2 - self.message_bg.get_width() // 2
                message_y = SCREEN_HEIGHT // 2 - self.message_bg.get_height() // 2
                self.screen.blit(self.message_bg, (message_x, message_y))
                self.screen.blit(self.message_text, (message_x + 20, message_y + 20))
                self.screen.blit(self.ok_button_bg, (self.ok_button_rect.x, self.ok_button_rect.y))
                self.screen.blit(self.ok_button_text, (self.ok_button_rect.x + 15, self.ok_button_rect.y + 5))

            # Hiển thị tọa độ chuột
            mouse_pos_text = self.mouse_pos_font.render(f"Mouse: {mouse_pos}", True, WHITE)
            mouse_pos_bg = pygame.Surface((150, 25))
            mouse_pos_bg.fill((50, 50, 50))
            self.screen.blit(mouse_pos_bg, (10, 10))
            self.screen.blit(mouse_pos_text, (15, 15))

            # Hiển thị số tiền hiện tại
            money_text = self.mouse_pos_font.render(f"Money: {self.game_state.player.money}", True, WHITE)
            money_bg = pygame.Surface((150, 25))
            money_bg.fill((50, 50, 50))
            self.screen.blit(money_bg, (10, 40))
            self.screen.blit(money_text, (15, 45))

            # Hiển thị thời gian hiện tại (ngày/đêm và thời gian còn lại)
            time_text = self.mouse_pos_font.render(
                f"Day: {self.game_state.time_system.current_day} | {self.game_state.time_system.get_time_of_day()} | Time Left: {self.game_state.time_system.format_time(self.game_state.time_system.get_remaining_time())}",
                True, WHITE
            )
            time_bg = pygame.Surface((300, 25))
            time_bg.fill((50, 50, 50))
            self.screen.blit(time_bg, (10, 70))
            self.screen.blit(time_text, (15, 75))

            # Vẽ UI (map, inventory, v.v.)
            self.ui.draw()

            pygame.display.flip()

    def handle_click(self, pos):
        # Kiểm tra nhấp vào ô "Thương nhân nông trại" (chỉ khi menu không hiển thị)
        if not self.show_menu and self.farmer_trader_rect.collidepoint(pos):
            self.show_menu = True
            self.current_menu = "menubanhat"  # Mở menu mua hạt giống mặc định
            self.update_menu_image()
        # Kiểm tra nhấp vào ô "Thương nhân câu cá" (chỉ khi menu không hiển thị)
        elif not self.show_menu and self.fisher_trader_rect.collidepoint(pos):
            self.show_menu = True
            self.current_menu = "menubanca"  # Mở menu bán cá mặc định
            self.update_menu_image()
        # Nếu menu đang hiển thị, xử lý nhấp chuột trên menu
        elif self.show_menu:
            # Xử lý nhấp vào nút "Thoát"
            if self.exit_button_rect.collidepoint(pos):
                self.show_menu = False
                print("Đã thoát menu!")
                return

            # Xử lý menu nông trại
            if self.current_menu in ["menubanhat", "menubanrau", "menumuadat"]:
                if self.buy_seed_rect.collidepoint(pos):
                    print("Bán nông sản")
                    self.current_menu = "menubanrau"
                    self.update_menu_image()
                elif self.sell_crop_rect.collidepoint(pos):
                    print("Mua hạt giống")
                    self.current_menu = "menubanhat"
                    self.update_menu_image()
                elif self.buy_farm_rect.collidepoint(pos):
                    print("Mua đất")
                    self.current_menu = "menumuadat"
                    self.update_menu_image()
            # Xử lý menu câu cá
            elif self.current_menu in ["menubanca", "menucancau"]:
                if self.sell_fish_rect.collidepoint(pos):
                    print("Bán cá")
                    self.current_menu = "menubanca"
                    self.update_menu_image()
                elif self.buy_rod_rect.collidepoint(pos):
                    print("Mua cần câu")
                    self.current_menu = "menucancau"
                    self.update_menu_image()

            # Xử lý nhấp chuột cho các loại hạt giống (chỉ khi ở menubanhat)
            if self.current_menu == "menubanhat":
                if self.cabbage_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(3):
                        self.game_state.player.inventory.add_item("cabbage_seed", 1)
                        print("Đã mua hạt bắp cải - 3 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.pumpkin_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(6):
                        self.game_state.player.inventory.add_item("pumpkin_seed", 1)
                        print("Đã mua hạt bí đỏ - 6 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.carrot_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(2):
                        self.game_state.player.inventory.add_item("carrot_seed", 1)
                        print("Đã mua hạt cà rốt - 2 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.beetroot_seed_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(5):
                        self.game_state.player.inventory.add_item("beetroot_seed", 1)
                        print("Đã mua hạt củ dền - 5 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.rare_herb_seed_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("frog", 5):
                        self.game_state.player.inventory.remove_item("frog", 5)
                        self.game_state.player.inventory.add_item("rare_herb_seed", 1)
                        print("Đã mua hạt thảo mộc hiếm - 5 ếch")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ ếch!", True, WHITE)
                elif self.energy_herb_seed_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("frog", 3):
                        self.game_state.player.inventory.remove_item("frog", 3)
                        self.game_state.player.inventory.add_item("energy_herb_seed", 1)
                        print("Đã mua hạt thảo mộc năng lượng - 3 ếch")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ ếch!", True, WHITE)

            # Xử lý nhấp chuột cho các loại nông sản (chỉ khi ở menubanrau)
            elif self.current_menu == "menubanrau":
                if self.cabbage_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("cabbage", 1):
                        self.game_state.player.inventory.remove_item("cabbage", 1)
                        self.game_state.player.add_money(4)
                        print("Đã bán bắp cải, nhận được 4 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có bắp cải để bán!", True, WHITE)
                elif self.pumpkin_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("pumpkin", 1):
                        self.game_state.player.inventory.remove_item("pumpkin", 1)
                        self.game_state.player.add_money(9)
                        print("Đã bán bí đỏ, nhận được 9 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có bí đỏ để bán!", True, WHITE)
                elif self.carrot_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("carrot", 1):
                        self.game_state.player.inventory.remove_item("carrot", 1)
                        self.game_state.player.add_money(3)
                        print("Đã bán cà rốt, nhận được 3 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có cà rốt để bán!", True, WHITE)
                elif self.beetroot_crop_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("beetroot", 1):
                        self.game_state.player.inventory.remove_item("beetroot", 1)
                        self.game_state.player.add_money(7)
                        print("Đã bán củ dền, nhận được 7 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có củ dền để bán!", True, WHITE)
                elif self.rare_herb_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("rare_herb", 1):
                        self.game_state.player.inventory.remove_item("rare_herb", 1)
                        self.game_state.player.add_money(15)
                        print("Đã bán thảo mộc hiếm, nhận được 15 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có thảo mộc hiếm để bán!", True, WHITE)
                elif self.energy_herb_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("energy_herb", 1):
                        self.game_state.player.inventory.remove_item("energy_herb", 1)
                        self.game_state.player.add_money(10)
                        print("Đã bán thảo mộc năng lượng, nhận được 10 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có thảo mộc năng lượng để bán!", True, WHITE)

            # Xử lý nhấp chuột cho các loại cá (chỉ khi ở menubanca)
            elif self.current_menu == "menubanca":
                if self.carophi_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("tilapia", 1):
                        self.game_state.player.inventory.remove_item("tilapia", 1)
                        self.game_state.player.add_money(5)
                        print("Đã bán cá rô phi, nhận được 5 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có cá rô phi để bán!", True, WHITE)
                elif self.cachep_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("carp", 1):
                        self.game_state.player.inventory.remove_item("carp", 1)
                        self.game_state.player.add_money(7)
                        print("Đã bán cá chép, nhận được 7 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có cá chép để bán!", True, WHITE)
                elif self.catre_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("catfish", 1):
                        self.game_state.player.inventory.remove_item("catfish", 1)
                        self.game_state.player.add_money(10)
                        print("Đã bán cá trê, nhận được 10 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có cá trê để bán!", True, WHITE)
                elif self.cachinh_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("eel", 1):
                        self.game_state.player.inventory.remove_item("eel", 1)
                        self.game_state.player.add_money(15)
                        print("Đã bán cá chình, nhận được 15 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có cá chình để bán!", True, WHITE)
                elif self.cama_rect.collidepoint(pos):
                    if self.game_state.player.inventory.has_item("ghost_fish", 1):
                        self.game_state.player.inventory.remove_item("ghost_fish", 1)
                        self.game_state.player.add_money(20)
                        print("Đã bán cá ma, nhận được 20 đồng!")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không có cá ma để bán!", True, WHITE)

            # Xử lý nhấp chuột cho các loại cần câu (chỉ khi ở menucancau)
            elif self.current_menu == "menucancau":
                if self.silver_rod_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(20):  # Kiểm tra và trừ tiền
                        self.game_state.player.upgrade_rod("silver")  # Cập nhật rod_level thành "silver"
                        print("Đã mua cần câu bạc - 20 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.gold_rod_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(50):  # Kiểm tra và trừ tiền
                        self.game_state.player.upgrade_rod("gold")  # Cập nhật rod_level thành "gold"
                        print("Đã mua cần câu vàng - 50 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.platinum_rod_rect.collidepoint(pos):
                    if self.game_state.player.spend_money(100):  # Kiểm tra và trừ tiền
                        self.game_state.player.upgrade_rod("diamond")  # Cập nhật rod_level thành "diamond"
                        print("Đã mua cần câu bạch kim - 100 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)

            # Xử lý nhấp chuột cho các tùy chọn mua đất (chỉ khi ở menumuadat)
            elif self.current_menu == "menumuadat":
                if self.expand_2_to_4_rect.collidepoint(pos):
                    if self.game_state.player.upgrade_garden(4):  # Mở rộng lên 4 ô
                        print("Đã mở rộng vườn từ 2 ô lên 4 ô - 18 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.expand_4_to_6_rect.collidepoint(pos):
                    if self.game_state.player.upgrade_garden(6):  # Mở rộng lên 6 ô
                        print("Đã mở rộng vườn từ 4 ô lên 6 ô - 25 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)
                elif self.expand_6_to_8_rect.collidepoint(pos):
                    if self.game_state.player.upgrade_garden(8):  # Mở rộng lên 8 ô
                        print("Đã mở rộng vườn từ 6 ô lên 8 ô - 32 đồng")
                    else:
                        self.show_message = True
                        self.message_text = self.tooltip_font.render("Không đủ tiền!", True, WHITE)

            # Đóng menu khi nhấp ra ngoài
            elif not self.menu_rect.collidepoint(pos):
                self.show_menu = False
                print("Đã thoát menu!")

    def update_menu_image(self):
        """Cập nhật hình ảnh menu dựa trên current_menu."""
        try:
            self.menu_image = pygame.image.load(self.menu_images[self.current_menu]).convert_alpha()
            self.menu_image = pygame.transform.scale(self.menu_image, (387, 539))
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.menu_images[self.current_menu]}")
            self.menu_image = pygame.Surface((387, 539))
            self.menu_image.fill((255, 0, 0))

        # Cập nhật lại vị trí và khu vực của menu sau khi thay đổi kích thước
        self.menu_x = (SCREEN_WIDTH - self.menu_image.get_width()) // 2
        self.menu_y = (SCREEN_HEIGHT - self.menu_image.get_height()) // 2
        self.menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_image.get_width(), self.menu_image.get_height())

        # Cập nhật lại vị trí các ô vuông trên menu
        self.buy_seed_rect = pygame.Rect(500, 109, 95, 65)
        self.sell_crop_rect = pygame.Rect(651, 109, 95, 65)
        self.buy_farm_rect = pygame.Rect(754, 204, 50, 90)
        self.sell_fish_rect = pygame.Rect(500, 109, 95, 65)
        self.buy_rod_rect = pygame.Rect(651, 109, 95, 65)