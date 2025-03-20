import pygame
from src.core.player import Player
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.scenes.fishing import FishingScene  # Chỉ giữ FishingScene

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

        # Các khu vực tương tác (chỉ giữ farmer_trader_rect và fisher_trader_rect)
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
            "carrot_seed": self.tooltip_font.render("Hạt cà rốt - 2 đồng", True, WHITE),
            "cabbage_seed": self.tooltip_font.render("Hạt bắp cải - 3 đồng", True, WHITE),
            "beetroot_seed": self.tooltip_font.render("Hạt củ dền - 5 đồng", True, WHITE),
            "pumpkin_seed": self.tooltip_font.render("Hạt bí đỏ - 6 đồng", True, WHITE),
            "carrot_crop": self.tooltip_font.render("Cà rốt - 3 đồng", True, WHITE),
            "cabbage_crop": self.tooltip_font.render("Bắp cải - 4 đồng", True, WHITE),
            "beetroot_crop": self.tooltip_font.render("Củ dền - 7 đồng", True, WHITE),
            "pumpkin_crop": self.tooltip_font.render("Bí đỏ - 9 đồng", True, WHITE),
            "rare_herb": self.tooltip_font.render("Thảo mộc hiếm - 15 đồng", True, WHITE),
            "expand_4_to_6": self.tooltip_font.render("Mở rộng 4 ô -> 6 ô - 18 đồng", True, WHITE),
            "expand_6_to_8": self.tooltip_font.render("Mở rộng 6 ô -> 8 ô - 25 đồng", True, WHITE),
            "expand_8_to_10": self.tooltip_font.render("Mở rộng 8 ô -> 10 ô - 32 đồng", True, WHITE),
        }
        self.tooltip_bg = pygame.Surface((200, 35))  # Tăng kích thước để vừa với tooltip dài hơn
        self.tooltip_bg.fill((50, 50, 50))

        # Font để hiển thị tọa độ chuột
        self.mouse_pos_font = pygame.font.SysFont(None, 25)

        # Tải các hình ảnh menu
        self.menu_images = {
            "menubanhat": "../../assets/images/fish/menubanhat.png",
            "menubanrau": "../../assets/images/fish/menubanrau.png",
            "menumuadat": "../../assets/images/fish/menumuadat.png"
        }
        self.current_menu = "menubanhat"  # Hình ảnh menu ban đầu

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
        self.buy_seed_rect = pygame.Rect(500, 109, 95, 65)  # Ô "Bán nông sản"
        self.sell_crop_rect = pygame.Rect(651, 109, 95, 65)  # Ô "Mua hạt giống"
        self.buy_farm_rect = pygame.Rect(754, 204, 50, 90)  # Ô "Mua đất"

        # Định nghĩa các ô vuông cho các loại hạt giống (hiển thị khi ở menubanhat)
        self.carrot_seed_rect = pygame.Rect(490, 249, 93, 80)  # Ô "Hạt cà rốt"
        self.cabbage_seed_rect = pygame.Rect(577, 249, 93, 80)  # Ô "Hạt bắp cải"
        self.beetroot_seed_rect = pygame.Rect(665, 249, 93, 80)  # Ô "Hạt củ dền"
        self.pumpkin_seed_rect = pygame.Rect(490, 357, 93, 80)  # Ô "Hạt bí đỏ"

        # Định nghĩa các ô vuông cho các loại nông sản (hiển thị khi ở menubanrau)
        self.carrot_crop_rect = pygame.Rect(490, 249, 93, 80)  # Ô "Cà rốt"
        self.cabbage_crop_rect = pygame.Rect(577, 249, 93, 80)  # Ô "Bắp cải"
        self.beetroot_crop_rect = pygame.Rect(665, 249, 93, 80)  # Ô "Củ dền"
        self.pumpkin_crop_rect = pygame.Rect(490, 357, 93, 80)  # Ô "Bí đỏ"
        self.rare_herb_rect = pygame.Rect(577, 357, 93, 80)  # Ô "Thảo mộc hiếm"

        # Định nghĩa các ô vuông cho các tùy chọn mua đất (hiển thị khi ở menumuadat)
        self.expand_4_to_6_rect = pygame.Rect(490, 249, 93, 80)  # Ô "Mở rộng 4 ô -> 6 ô"
        self.expand_6_to_8_rect = pygame.Rect(577, 249, 93, 80)  # Ô "Mở rộng 6 ô -> 8 ô"
        self.expand_8_to_10_rect = pygame.Rect(665, 249, 93, 80)  # Ô "Mở rộng 8 ô -> 10 ô"

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
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_message:
                        # Xử lý nhấp chuột vào nút OK
                        if self.ok_button_rect.collidepoint(mouse_pos):
                            self.show_message = False
                    else:
                        self.handle_click(mouse_pos)

            # Vẽ background
            time_of_day = self.time_system.get_time_of_day()
            if time_of_day == "day":
                self.screen.blit(self.day_background, (0, 0))
            elif time_of_day == "night":
                self.screen.blit(self.night_background, (0, 0))

            # Vẽ menu nếu đang hiển thị
            if self.show_menu:
                self.screen.blit(self.menu_image, (self.menu_x, self.menu_y))

            # Hiển thị tooltip cho các khu vực tương tác (chỉ khi menu không hiển thị và không có thông báo)
            if not self.show_menu and not self.show_message:
                for rect, name in [(self.farmer_trader_rect, "farmer_trader"),
                                   (self.fisher_trader_rect, "fisher_trader")]:
                    if rect.collidepoint(mouse_pos):
                        tooltip_x = rect.x
                        tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                        self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                        self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

            # Hiển thị tooltip cho các ô vuông trong menu (chỉ khi menu hiển thị và không có thông báo)
            if self.show_menu and not self.show_message:
                for rect, name in [(self.buy_seed_rect, "buy_seed"),
                                   (self.sell_crop_rect, "sell_crop"),
                                   (self.buy_farm_rect, "buy_farm")]:
                    if rect.collidepoint(mouse_pos):
                        tooltip_x = rect.x
                        tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                        self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                        self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                # Hiển thị tooltip cho các loại hạt giống (chỉ khi ở menubanhat)
                if self.current_menu == "menubanhat":
                    for rect, name in [(self.carrot_seed_rect, "carrot_seed"),
                                       (self.cabbage_seed_rect, "cabbage_seed"),
                                       (self.beetroot_seed_rect, "beetroot_seed"),
                                       (self.pumpkin_seed_rect, "pumpkin_seed")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                # Hiển thị tooltip cho các loại nông sản (chỉ khi ở menubanrau)
                if self.current_menu == "menubanrau":
                    for rect, name in [(self.carrot_crop_rect, "carrot_crop"),
                                       (self.cabbage_crop_rect, "cabbage_crop"),
                                       (self.beetroot_crop_rect, "beetroot_crop"),
                                       (self.pumpkin_crop_rect, "pumpkin_crop"),
                                       (self.rare_herb_rect, "rare_herb")]:
                        if rect.collidepoint(mouse_pos):
                            tooltip_x = rect.x
                            tooltip_y = rect.y - self.tooltip_bg.get_height() - 5
                            self.screen.blit(self.tooltip_bg, (tooltip_x, tooltip_y))
                            self.screen.blit(self.tooltips[name], (tooltip_x + 5, tooltip_y + 5))

                # Hiển thị tooltip cho các tùy chọn mua đất (chỉ khi ở menumuadat)
                if self.current_menu == "menumuadat":
                    for rect, name in [(self.expand_4_to_6_rect, "expand_4_to_6"),
                                       (self.expand_6_to_8_rect, "expand_6_to_8"),
                                       (self.expand_8_to_10_rect, "expand_8_to_10")]:
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

            # Hiển thị tọa độ chuột ở góc trên bên trái
            mouse_pos_text = self.mouse_pos_font.render(f"Mouse: {mouse_pos}", True, WHITE)
            mouse_pos_bg = pygame.Surface((150, 25))
            mouse_pos_bg.fill((50, 50, 50))
            self.screen.blit(mouse_pos_bg, (10, 10))
            self.screen.blit(mouse_pos_text, (15, 15))

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        # Kiểm tra nhấp vào ô "Thương nhân nông trại" (chỉ khi menu không hiển thị)
        if not self.show_menu and self.farmer_trader_rect.collidepoint(pos):
            self.show_menu = True
        # Nếu menu đang hiển thị, xử lý nhấp chuột trên menu
        elif self.show_menu:
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
            # Xử lý nhấp chuột cho các loại hạt giống (chỉ khi ở menubanhat)
            elif self.current_menu == "menubanhat":
                if self.carrot_seed_rect.collidepoint(pos):
                    if self.player.money >= 2:
                        self.player.money -= 2
                        print("Đã mua hạt cà rốt - 2 đồng")
                    else:
                        self.show_message = True
                elif self.cabbage_seed_rect.collidepoint(pos):
                    if self.player.money >= 3:
                        self.player.money -= 3
                        print("Đã mua hạt bắp cải - 3 đồng")
                    else:
                        self.show_message = True
                elif self.beetroot_seed_rect.collidepoint(pos):
                    if self.player.money >= 5:
                        self.player.money -= 5
                        print("Đã mua hạt củ dền - 5 đồng")
                    else:
                        self.show_message = True
                elif self.pumpkin_seed_rect.collidepoint(pos):
                    if self.player.money >= 6:
                        self.player.money -= 6
                        print("Đã mua hạt bí đỏ - 6 đồng")
                    else:
                        self.show_message = True
            # Xử lý nhấp chuột cho các loại nông sản (chỉ khi ở menubanrau)
            elif self.current_menu == "menubanrau":
                if self.carrot_crop_rect.collidepoint(pos):
                    print("Bán cà rốt - 3 đồng")
                elif self.cabbage_crop_rect.collidepoint(pos):
                    print("Bán bắp cải - 4 đồng")
                elif self.beetroot_crop_rect.collidepoint(pos):
                    print("Bán củ dền - 7 đồng")
                elif self.pumpkin_crop_rect.collidepoint(pos):
                    print("Bán bí đỏ - 9 đồng")
                elif self.rare_herb_rect.collidepoint(pos):
                    print("Bán thảo mộc hiếm - 15 đồng")
            # Xử lý nhấp chuột cho các tùy chọn mua đất (chỉ khi ở menumuadat)
            elif self.current_menu == "menumuadat":
                if self.expand_4_to_6_rect.collidepoint(pos):
                    if self.player.money >= 18:
                        self.player.money -= 18
                        print("Đã mở rộng vườn từ 4 ô lên 6 ô - 18 đồng")
                    else:
                        self.show_message = True
                elif self.expand_6_to_8_rect.collidepoint(pos):
                    if self.player.money >= 25:
                        self.player.money -= 25
                        print("Đã mở rộng vườn từ 6 ô lên 8 ô - 25 đồng")
                    else:
                        self.show_message = True
                elif self.expand_8_to_10_rect.collidepoint(pos):
                    if self.player.money >= 32:
                        self.player.money -= 32
                        print("Đã mở rộng vườn từ 8 ô lên 10 ô - 32 đồng")
                    else:
                        self.show_message = True
            elif not self.menu_rect.collidepoint(pos):
                self.show_menu = False  # Đóng menu khi nhấp ra ngoài
        # Xử lý nhấp chuột khác (chỉ khi menu không hiển thị)
        elif not self.show_menu and self.fisher_trader_rect.collidepoint(pos):
            print("Mở menu thương nhân câu cá!")

    def update_menu_image(self):
        """Cập nhật hình ảnh menu dựa trên current_menu."""
        try:
            self.menu_image = pygame.image.load(self.menu_images[self.current_menu]).convert_alpha()
            # Kiểm tra nếu là menumuadat.png thì đặt kích thước là (387, 600)
            if self.current_menu == "menumuadat":
                self.menu_image = pygame.transform.scale(self.menu_image, (387, 539))
            else:
                self.menu_image = pygame.transform.scale(self.menu_image, (387, 539))
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.menu_images[self.current_menu]}")
            # Nếu lỗi, đặt kích thước mặc định dựa trên current_menu
            if self.current_menu == "menumuadat":
                self.menu_image = pygame.Surface((387, 600))
            else:
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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    from src.core.player import Player

    class FakeTimeSystem:
        def get_time_of_day(self):
            return "night"

    player = Player()
    player.add_money(5)  # Thêm 5 đồng để thử nghiệm (ít hơn giá mua đất và một số hạt giống)
    time_system = FakeTimeSystem()
    village_scene = VillageScene(player, time_system, screen)
    village_scene.run()
    pygame.quit()