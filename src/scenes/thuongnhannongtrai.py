import pygame
from src.core.player import Player
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class ThuongNhanNongTraiScene:
    def __init__(self, player, time_system, screen):
        self.player = player
        self.time_system = time_system
        self.screen = screen
        pygame.display.set_caption("Thương nhân nông trại")

        # Background tạm
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))  # Nền đen

        # Định nghĩa các khung (vị trí giữ nguyên)
        self.sell_frame = pygame.Rect(50, 50, 300, 200)   # Khung bán nông sản
        self.buy_frame = pygame.Rect(400, 50, 300, 200)   # Khung mua hạt giống
        self.expand_frame = pygame.Rect(50, 300, 300, 200) # Khung mở rộng vườn
        self.info_frame = pygame.Rect(400, 300, 300, 200)  # Khung thông tin
        self.back_button = pygame.Rect(350, 550, 100, 100) # Nút quay lại

        # Tải hình ảnh menu (thay đường dẫn bằng đường dẫn thực tế của bạn)
        try:
            self.sell_image = pygame.image.load("D:/Python game/doAnPython/assets/images/menus/sell_frame.png").convert_alpha()
            self.buy_image = pygame.image.load("D:/Python game/doAnPython/assets/images/menus/buy_frame.png").convert_alpha()
            self.expand_image = pygame.image.load("D:/Python game/doAnPython/assets/images/menus/expand_frame.png").convert_alpha()
            self.info_image = pygame.image.load("D:/Python game/doAnPython/assets/images/menus/info_frame.png").convert_alpha()
            self.back_image = pygame.image.load("D:/Python game/doAnPython/assets/images/menus/back_button.png").convert_alpha()

            # Điều chỉnh kích thước hình ảnh để khớp với Rect
            self.sell_image = pygame.transform.scale(self.sell_image, (self.sell_frame.width, self.sell_frame.height))
            self.buy_image = pygame.transform.scale(self.buy_image, (self.buy_frame.width, self.buy_frame.height))
            self.expand_image = pygame.transform.scale(self.expand_image, (self.expand_frame.width, self.expand_frame.height))
            self.info_image = pygame.transform.scale(self.info_image, (self.info_frame.width, self.info_frame.height))
            self.back_image = pygame.transform.scale(self.back_image, (self.back_button.width, self.back_button.height))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file hình ảnh - {e}")
            # Sử dụng hình ảnh mặc định thay vì màu tím
            default_image_path = "D:/Python game/doAnPython/assets/images/backgrounds/background-cauca-dem.png"  # Đường dẫn đến hình ảnh mặc định
            default_image = pygame.image.load(default_image_path).convert_alpha()
            # Scale hình ảnh mặc định để khớp với kích thước khung
            self.sell_image = pygame.transform.scale(default_image, (self.sell_frame.width, self.sell_frame.height))
            self.buy_image = pygame.transform.scale(default_image, (self.buy_frame.width, self.buy_frame.height))
            self.expand_image = pygame.transform.scale(default_image, (self.expand_frame.width, self.expand_frame.height))
            self.info_image = pygame.transform.scale(default_image, (self.info_frame.width, self.info_frame.height))
            self.back_image = pygame.transform.scale(default_image, (self.back_button.width, self.back_button.height))

        # Icon nông sản, hạt giống và mở rộng vườn (giả định, thay bằng ảnh thực tế)
        self.icons = {
            "carrot": pygame.Surface((50, 50)), "cabbage": pygame.Surface((50, 50)),
            "tomato": pygame.Surface((50, 50)), "potato": pygame.Surface((50, 50)),
            "carrot_seed": pygame.Surface((50, 50)), "cabbage_seed": pygame.Surface((50, 50)),
            "tomato_seed": pygame.Surface((50, 50)), "potato_seed": pygame.Surface((50, 50)),
            "rare_herb": pygame.Surface((50, 50)),
            "expand_4_to_6": pygame.Surface((50, 50)), "expand_6_to_8": pygame.Surface((50, 50)),
            "expand_8_to_10": pygame.Surface((50, 50))
        }
        for item, icon in self.icons.items():
            if "expand" in item:
                icon.fill((0, 255, 0))  # Màu xanh lá
            elif "seed" in item:
                icon.fill((255, 255, 0))  # Màu vàng
            else:
                icon.fill((255, 0, 0))  # Màu đỏ

        # Vị trí icon trong khung bán
        self.sell_icon_positions = [
            (100, 100), (170, 100), (240, 100), (310, 100)
        ]
        # Vị trí icon trong khung mua
        self.buy_icon_positions = [
            (450, 100), (520, 100), (590, 100), (660, 100), (450, 170)
        ]
        # Vị trí icon trong khung mở rộng vườn
        self.expand_icon_positions = [
            (100, 350), (170, 350), (240, 350)
        ]

        # Font
        self.font = pygame.font.SysFont(None, 30)
        self.back_text = self.font.render("Quay lại", True, WHITE)

        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(mouse_pos)

            # Vẽ giao diện
            self.screen.blit(self.background, (0, 0))

            # Vẽ các khung bằng hình ảnh
            self.screen.blit(self.sell_image, self.sell_frame.topleft)
            self.screen.blit(self.buy_image, self.buy_frame.topleft)
            self.screen.blit(self.expand_image, self.expand_frame.topleft)
            self.screen.blit(self.info_image, self.info_frame.topleft)
            self.screen.blit(self.back_image, self.back_button.topleft)

            # Vẽ icon bán
            sell_items = ["carrot", "cabbage", "tomato", "potato"]
            for (x, y), item in zip(self.sell_icon_positions, sell_items):
                self.screen.blit(self.icons[item], (x, y))

            # Vẽ icon mua
            buy_items = ["carrot_seed", "cabbage_seed", "tomato_seed", "potato_seed", "rare_herb"]
            for (x, y), item in zip(self.buy_icon_positions, buy_items):
                self.screen.blit(self.icons[item], (x, y))

            # Vẽ icon mở rộng vườn
            expand_items = ["expand_4_to_6", "expand_6_to_8", "expand_8_to_10"]
            for (x, y), item in zip(self.expand_icon_positions, expand_items):
                self.screen.blit(self.icons[item], (x, y))

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        if self.back_button.collidepoint(pos):
            print("Quay lại làng!")
            self.running = False
        # Xử lý click vào icon bán
        sell_items = ["carrot", "cabbage", "tomato", "potato"]
        for (x, y), item in zip(self.sell_icon_positions, sell_items):
            icon_rect = pygame.Rect(x, y, 50, 50)
            if icon_rect.collidepoint(pos):
                self.sell_item(item)
                return
        # Xử lý click vào icon mua
        buy_items = ["carrot_seed", "cabbage_seed", "tomato_seed", "potato_seed", "rare_herb"]
        for (x, y), item in zip(self.buy_icon_positions, buy_items):
            icon_rect = pygame.Rect(x, y, 50, 50)
            if icon_rect.collidepoint(pos):
                self.buy_item(item)
                return
        # Xử lý click vào icon mở rộng vườn
        expand_items = ["expand_4_to_6", "expand_6_to_8", "expand_8_to_10"]
        for (x, y), item in zip(self.expand_icon_positions, expand_items):
            icon_rect = pygame.Rect(x, y, 50, 50)
            if icon_rect.collidepoint(pos):
                self.expand_garden(item)
                return

    def sell_item(self, item):
        prices = {"carrot": 3, "cabbage": 4, "tomato": 7, "potato": 9}
        if item in prices and self.player.inventory.remove_item(item, 1):
            self.player.add_money(prices[item])
            print(f"Đã bán {item} với giá {prices[item]} đồng!")

    def buy_item(self, item):
        prices = {"carrot_seed": 2, "cabbage_seed": 3, "tomato_seed": 5, "potato_seed": 6, "rare_herb": 15}
        if item in prices and self.player.spend_money(prices[item]):
            self.player.inventory.add_item(item, 1)
            print(f"Đã mua {item} với giá {prices[item]} đồng!")

    def expand_garden(self, action):
        if action == "expand_4_to_6":
            self.player.upgrade_garden(6)
        elif action == "expand_6_to_8":
            self.player.upgrade_garden(8)
        elif action == "expand_8_to_10":
            self.player.upgrade_garden(10)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    from src.core.player import Player

    class FakeTimeSystem:
        def get_time_of_day(self):
            return "day"

    player = Player()
    player.add_money(50)
    time_system = FakeTimeSystem()
    scene = ThuongNhanNongTraiScene(player, time_system, screen)
    scene.run()
    pygame.quit()