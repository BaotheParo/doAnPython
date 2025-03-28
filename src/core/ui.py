# import pygame
# import sys
# import os
# import json

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# IMAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "assets", "images"))

# from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

# class SettingsUI:
#     def __init__(self, screen, game_state):
#         self.screen = screen
#         self.game_state = game_state  # GameState có các hàm save_game() và quản lý current_scene
#         self.show_menu = False
#         self.show_map = False
#         self.running = True

#         self.screen_width, self.screen_height = self.screen.get_size()
#         self.menu_width = int(self.screen_width * 0.25)
#         self.menu_height = int(self.screen_height * 0.3)
#         self.menu_x = (self.screen_width - self.menu_width) // 2
#         self.menu_y = (self.screen_height - self.menu_height) // 2

#         self.map_width = int(self.screen_width * 0.5)
#         self.map_height = int(self.screen_height * 0.5)
#         self.map_x = (self.screen_width - self.map_width) // 2
#         self.map_y = (self.screen_height - self.map_height) // 2

#         # Vùng ngôi làng trên ảnh map (tọa độ tương đối)
#         self.village_rect_rel = pygame.Rect(30, 20, 235, 130)
#         self.on_village_click = self.go_to_village_scene

#         # Vùng ao cá trên ảnh map (tọa độ tương đối)
#         self.fish_rect_rel = pygame.Rect(345, 180, 235, 100)
#         self.on_fish_click = self.go_to_fishing_scene

#         self.farm_rect_rel = pygame.Rect(154, 225, 120, 100)
#         self.on_farm_click = self.go_to_farm_scene

#         self.icon_settings = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "SettingBtn.png")).convert_alpha()
#         self.icon_settings = pygame.transform.scale(self.icon_settings, (50, 50))
#         self.icon_settings_rect = self.icon_settings.get_rect(topleft=(self.screen_width - 80, 20))

#         self.icon_map = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "mapBtn.png")).convert_alpha()
#         self.icon_map = pygame.transform.scale(self.icon_map, (50, 50))
#         self.icon_map_rect = self.icon_map.get_rect(topleft=(self.screen_width - 150, 20))

#         self.icon_inventory = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-tuido.png")).convert_alpha()
#         self.icon_inventory = pygame.transform.scale(self.icon_inventory, (50, 50))
#         self.icon_inventory_rect = self.icon_inventory.get_rect(topleft=(self.screen_width - 220, 20))

#         self.map_image = pygame.image.load(os.path.join(IMAGE_DIR, "backgrounds", "map.png")).convert_alpha()
#         self.map_image = pygame.transform.scale(self.map_image, (self.map_width, self.map_height))

#         self.back_icon = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-quaylai.png")).convert_alpha()
#         self.back_icon = pygame.transform.scale(self.back_icon, (40, 40))

#         self.font = pygame.font.Font(None, int(self.screen_width * 0.02))

#         self.button_width = int(self.menu_width * 0.8)
#         self.button_height = int(self.menu_height * 0.2)
#         self.buttons = [
#             {"text": "Save Game", "action": self.save_game_ui,
#              "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
#             {"text": "Main Menu", "action": self.main_menu_ui,
#              "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
#             {"text": "Exit Game", "action": self.exit_game,
#              "rect": pygame.Rect(0, 0, self.button_width, self.button_height)}
#         ]

#     def draw(self):
#         # Vẽ icon UI: Settings, Map, Inventory
#         self.screen.blit(self.icon_settings, self.icon_settings_rect)
#         self.screen.blit(self.icon_map, self.icon_map_rect)
#         self.screen.blit(self.icon_inventory, self.icon_inventory_rect)

#         # Vẽ menu Settings nếu mở
#         if self.show_menu:
#             pygame.draw.rect(self.screen, (50, 50, 50),
#                              (self.menu_x, self.menu_y, self.menu_width, self.menu_height))
#             pygame.draw.rect(self.screen, (255, 255, 255),
#                              (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 3)
#             for i, button in enumerate(self.buttons):
#                 button_x = self.menu_x + (self.menu_width - self.button_width) // 2
#                 button_y = self.menu_y + 20 + i * (self.button_height + 10)
#                 button["rect"].topleft = (button_x, button_y)
#                 color = (150, 150, 150) if button["rect"].collidepoint(pygame.mouse.get_pos()) else (100, 100, 100)
#                 pygame.draw.rect(self.screen, color, button["rect"])
#                 pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2)
#                 text_surface = self.font.render(button["text"], True, (255, 255, 255))
#                 text_rect = text_surface.get_rect(center=button["rect"].center)
#                 self.screen.blit(text_surface, text_rect)

#         # Vẽ popup Map nếu mở
#         if self.show_map:
#             border_x = self.map_x - 4
#             border_y = self.map_y - 4
#             border_w = self.map_width + 8
#             border_h = self.map_height + 8
#             pygame.draw.rect(self.screen, (155, 173, 183),
#                              (border_x, border_y, border_w, border_h), width=4)
#             pygame.draw.rect(self.screen, (50, 50, 50),
#                              (self.map_x, self.map_y, self.map_width, self.map_height))
#             self.screen.blit(self.map_image, (self.map_x, self.map_y))
#             self.back_icon_rect = self.back_icon.get_rect(topright=(self.map_x + self.map_width - 10, self.map_y + 10))
#             self.screen.blit(self.back_icon, self.back_icon_rect)

#             # Tính toán vùng ngôi làng và ao cá dựa trên vị trí hiện tại của map
#             village_rect = pygame.Rect(
#                 self.map_x + self.village_rect_rel.x,
#                 self.map_y + self.village_rect_rel.y,
#                 self.village_rect_rel.width,
#                 self.village_rect_rel.height
#             )
#             fish_rect = pygame.Rect(
#                 self.map_x + self.fish_rect_rel.x,
#                 self.map_y + self.fish_rect_rel.y,
#                 self.fish_rect_rel.width,
#                 self.fish_rect_rel.height
#             )
#             farm_rect = pygame.Rect(
#                 self.map_x + self.farm_rect_rel.x,
#                 self.map_y + self.farm_rect_rel.y,
#                 self.farm_rect_rel.width,
#                 self.farm_rect_rel.height
#             )

#             # Đổi con trỏ chuột khi hover qua các vùng
#             mouse_pos = pygame.mouse.get_pos()
#             if village_rect.collidepoint(mouse_pos) or fish_rect.collidepoint(mouse_pos) or farm_rect.collidepoint(mouse_pos):
#                 pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
#             else:
#                 pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
#             # (Tuỳ chọn: vẽ viền debug)
#             # pygame.draw.rect(self.screen, (255, 0, 0), village_rect, 1)
#             # pygame.draw.rect(self.screen, (0, 255, 0), fish_rect, 1)
#             # pygame.draw.rect(self.screen, (0, 255, 0), farm_rect, 1)

#     def handle_event(self, event):
#         if event.type == pygame.QUIT:
#             self.running = False  # Thoát vòng lặp chính
#             pygame.quit()  # Đóng Pygame
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             # Nếu bấm icon Settings -> bật/tắt menu Settings
#             if self.icon_settings_rect.collidepoint(event.pos):
#                 self.show_menu = not self.show_menu
#                 self.show_map = False
#                 return True
#             # Nếu bấm icon Map -> bật/tắt popup Map
#             if self.icon_map_rect.collidepoint(event.pos):
#                 self.show_map = not self.show_map
#                 self.show_menu = False
#                 return True
#             # Nếu popup Map mở, chặn các event cho giao diện nền
#             if self.show_map:
#                 if self.back_icon_rect.collidepoint(event.pos):
#                     self.show_map = False
#                     return True
#                 village_rect = pygame.Rect(
#                     self.map_x + self.village_rect_rel.x,
#                     self.map_y + self.village_rect_rel.y,
#                     self.village_rect_rel.width,
#                     self.village_rect_rel.height
#                 )
#                 if village_rect.collidepoint(event.pos):
#                     print("Chuyển sang giao diện Làng!")
#                     self.on_village_click()
#                     return True
#                 fish_rect = pygame.Rect(
#                     self.map_x + self.fish_rect_rel.x,
#                     self.map_y + self.fish_rect_rel.y,
#                     self.fish_rect_rel.width,
#                     self.fish_rect_rel.height
#                 )
#                 if fish_rect.collidepoint(event.pos):
#                     print("Chuyển sang giao diện Câu Cá!")
#                     self.on_fish_click()
#                     return True
#                 farm_rect = pygame.Rect(
#                     self.map_x + self.farm_rect_rel.x,
#                     self.map_y + self.farm_rect_rel.y,
#                     self.farm_rect_rel.width,
#                     self.farm_rect_rel.height
#                 )
#                 if farm_rect.collidepoint(event.pos):
#                     print("Chuyển sang giao diện farm!")
#                     self.on_farm_click()
#                     return True
#                 # Nếu click vào bất kỳ vùng nào khác trên popup Map thì chặn event
#                 return True

#             # Nếu menu Settings mở, xử lý các nút
#             if self.show_menu:
#                 for button in self.buttons:
#                     if button["rect"].collidepoint(event.pos):
#                         button["action"]()
#                         return True

#         return False

#     def go_to_village_scene(self):
#         print("Yêu cầu chuyển sang giao diện Làng!")
#         self.running = False
#         from src.scenes.village import VillageScene
#         village_scene = VillageScene(self.game_state, self.screen,  self)
#         village_scene.run()


#     def go_to_fishing_scene(self):
#         from src.scenes.fishing import FishingScene
#         print("Chuyển đến FishingScene!")
#         # self.running = False
#         fishing_scene = FishingScene(self.game_state, self.screen, self)
#         fishing_scene.run()

#     def go_to_farm_scene(self):
#         from src.scenes.farm import FarmScene
#         print("Chuyển đến FarmScene!")
#         # self.running = False
#         farm_scene = FarmScene(self.game_state, self.screen, self)
#         farm_scene.run()

#     def save_game_ui(self):
#         self.game_state.save_game()
#         print("Game đã được lưu từ UI!")
#         self.show_menu = False

#     def main_menu_ui(self):
#         print("Quay về Main Menu...")
#         self.show_menu = False

#     def exit_game(self):
#         print("Thoát game!")
#         pygame.quit()
#         sys.exit()

# def start_ui(game_state):
#     pygame.init()
#     screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
#     pygame.display.set_caption("UI Settings")
#     settings_ui = SettingsUI(screen, game_state)
#     clock = pygame.time.Clock()
#     running = True

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.VIDEORESIZE:
#                 screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
#                 settings_ui = SettingsUI(screen, game_state)
#             settings_ui.handle_event(event)

#         screen.fill((0, 0, 0))
#         settings_ui.draw()
#         pygame.display.flip()
#         clock.tick(60)

#     pygame.quit()
#     sys.exit()

# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
#     from src.core.game_state import GameState
#     game_state = GameState()
#     start_ui(game_state)


import pygame
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
IMAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "assets", "images"))

from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

# Cấu hình Inventory
INV_COLS = 6         # Số cột trong kho đồ
INV_ROWS = 4         # Số hàng trong kho đồ
SLOT_WIDTH = 80      # Chiều rộng mỗi ô (slot)
SLOT_HEIGHT = 80     # Chiều cao mỗi ô (slot)
SLOT_MARGIN = 28      # Khoảng cách giữa các ô

# Dictionary ánh xạ tên vật phẩm sang đường dẫn icon (chỉnh sửa đường dẫn cho phù hợp)
item_icons = {
    "carrot_seed": os.path.join(IMAGE_DIR, "plants", "seed.png"),
    "cabbage_seed": os.path.join(IMAGE_DIR, "plants", "seed.png"),
    "beetroot_seed": os.path.join(IMAGE_DIR, "plants", "seed.png"),
    "pumpkin_seed": os.path.join(IMAGE_DIR, "plants", "seed.png"),
    "energy_herb_seed": os.path.join(IMAGE_DIR, "plants", "seed.png"),
    "rare_herb_seed": os.path.join(IMAGE_DIR, "plants", "seed.png"),
    "carrot": os.path.join(IMAGE_DIR, "plants", "carot.png"),
    "cabbage": os.path.join(IMAGE_DIR, "plants", "bapcai.png"),
    "tomato": os.path.join(IMAGE_DIR, "plants", "tomato.png"),
    "potato": os.path.join(IMAGE_DIR, "plants", "potato.png"),
    "beetroot": os.path.join(IMAGE_DIR, "plants", "cuden.png"),
    "pumpkin": os.path.join(IMAGE_DIR, "plants", "bido.png"),
    "energy_herb": os.path.join(IMAGE_DIR, "plants", "thaomoc.png"),
    "rare_herb": os.path.join(IMAGE_DIR, "plants", "lua.png"),
    "tilapia": os.path.join(IMAGE_DIR, "fish", "caRoPhi.png"),
    "carp": os.path.join(IMAGE_DIR, "fish", "caChep.png"),
    "catfish": os.path.join(IMAGE_DIR, "fish", "caTre.png"),
    "eel": os.path.join(IMAGE_DIR, "fish", "caChinh.png"),
    "ghost_fish": os.path.join(IMAGE_DIR, "fish", "caMa.png"),
    "frog": os.path.join(IMAGE_DIR, "fish", "ech.png"),
    "basic_rod": os.path.join(IMAGE_DIR, "fish", "caucaubac.png"),
    "silver_rod": os.path.join(IMAGE_DIR, "fish", "caucaubac.png"),
    "gold_rod": os.path.join(IMAGE_DIR, "fish", "cancauvang.png"),
    "diamond_rod": os.path.join(IMAGE_DIR, "fish", "cancaukimcuong.png")
}

class SettingsUI:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state  # GameState có các hàm save_game() và quản lý current_scene
        self.show_menu = False
        self.show_map = False
        self.show_inventory = False
        self.running = True

        self.screen_width, self.screen_height = self.screen.get_size()
        self.menu_width = int(self.screen_width * 0.25)
        self.menu_height = int(self.screen_height * 0.3)
        self.menu_x = (self.screen_width - self.menu_width) // 2
        self.menu_y = (self.screen_height - self.menu_height) // 2

        self.map_width = int(self.screen_width * 0.5)
        self.map_height = int(self.screen_height * 0.5)
        self.map_x = (self.screen_width - self.map_width) // 2
        self.map_y = (self.screen_height - self.map_height) // 2

        # self.inventory_width = int(SCREEN_WIDTH * 0.4)
        # self.inventory_height = int(SCREEN_HEIGHT * 0.4)
        self.inventory_width = 672
        self.inventory_height = 576
        self.inventory_x = (SCREEN_WIDTH - self.inventory_width) // 2
        self.inventory_y = (SCREEN_HEIGHT - self.inventory_height) // 2

        # Map regions (tọa độ tương đối trên ảnh map)
        self.village_rect_rel = pygame.Rect(30, 20, 235, 130)
        self.on_village_click = self.go_to_village_scene

        self.fish_rect_rel = pygame.Rect(345, 180, 235, 100)
        self.on_fish_click = self.go_to_fishing_scene

        self.farm_rect_rel = pygame.Rect(154, 225, 120, 100)
        self.on_farm_click = self.go_to_farm_scene

        self.icon_settings = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "SettingBtn.png")).convert_alpha()
        self.icon_settings = pygame.transform.scale(self.icon_settings, (50, 50))
        self.icon_settings_rect = self.icon_settings.get_rect(topleft=(self.screen_width - 80, 20))

        self.icon_map = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "mapBtn.png")).convert_alpha()
        self.icon_map = pygame.transform.scale(self.icon_map, (50, 50))
        self.icon_map_rect = self.icon_map.get_rect(topleft=(self.screen_width - 150, 20))

        self.icon_inventory = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-tuido.png")).convert_alpha()
        self.icon_inventory = pygame.transform.scale(self.icon_inventory, (50, 50))
        self.icon_inventory_rect = self.icon_inventory.get_rect(topleft=(self.screen_width - 220, 20))

        self.map_image = pygame.image.load(os.path.join(IMAGE_DIR, "backgrounds", "map.png")).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.map_width, self.map_height))

        self.back_icon = pygame.image.load(os.path.join(IMAGE_DIR, "icons", "icon-quaylai.png")).convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (40, 40))

        # Load background của popup Inventory
        inventory_bg_path = os.path.join(IMAGE_DIR, "backgrounds", "inventory3.png")
        try:
            self.inventory_image = pygame.image.load(inventory_bg_path).convert_alpha()
            self.inventory_image = pygame.transform.scale(self.inventory_image, (self.inventory_width, self.inventory_height))
        except FileNotFoundError:
            self.inventory_image = pygame.Surface((self.inventory_width, self.inventory_height), pygame.SRCALPHA)
            self.inventory_image.fill((80, 50, 50, 200))
        self.inventory_bg_rect = pygame.Rect(self.inventory_x, self.inventory_y, self.inventory_width, self.inventory_height)
        self.back_inv_icon_rect = self.back_icon.get_rect(topright=(self.inventory_bg_rect.right - 10, self.inventory_bg_rect.top + 10))

        self.font = pygame.font.Font(None, int(self.screen_width * 0.02))

        self.button_width = int(self.menu_width * 0.8)
        self.button_height = int(self.menu_height * 0.2)
        self.buttons = [
            {"text": "Save Game", "action": self.save_game_ui,
             "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
            {"text": "Main Menu", "action": self.main_menu_ui,
             "rect": pygame.Rect(0, 0, self.button_width, self.button_height)},
            {"text": "Exit Game", "action": self.exit_game,
             "rect": pygame.Rect(0, 0, self.button_width, self.button_height)}
        ]

        # Cấu hình Inventory: 6 cột, 4 hàng, mỗi ô 60x40, khoảng cách giữa các ô
        self.inv_cols = INV_COLS  # 6
        self.inv_rows = INV_ROWS  # 4
        self.slot_width = SLOT_WIDTH  # 60
        self.slot_height = SLOT_HEIGHT  # 40
        self.slot_margin = SLOT_MARGIN  # 8
        self.inventory_slots = []
        start_x = self.inventory_x + 25
        start_y = self.inventory_y + 140
        for row in range(self.inv_rows):
            for col in range(self.inv_cols):
                slot_x = start_x + col * (self.slot_width + self.slot_margin)
                slot_y = start_y + row * (self.slot_height + self.slot_margin)
                self.inventory_slots.append(pygame.Rect(slot_x, slot_y, self.slot_width, self.slot_height))

        # Load icon cho các vật phẩm trong Inventory
        self.item_icons = {}
        self.load_item_icons()

    def load_item_icons(self):
        """Tải icon cho các item từ dictionary item_icons đã khai báo"""
        for item, path in item_icons.items():
            try:
                img = pygame.image.load(path).convert_alpha()
                # Scale icon sao cho vừa slot (có padding 4 pixel mỗi bên)
                img = pygame.transform.scale(img, (self.slot_width - 4, self.slot_height - 4))
                self.item_icons[item] = img
            except FileNotFoundError:
                surf = pygame.Surface((self.slot_width - 4, self.slot_height - 4), pygame.SRCALPHA)
                surf.fill((255, 0, 0))
                self.item_icons[item] = surf

    def draw_inventory(self):
        """Vẽ popup Inventory với các ô và vật phẩm từ kho"""
        self.screen.blit(self.inventory_image, (self.inventory_bg_rect.x, self.inventory_bg_rect.y))
        self.screen.blit(self.back_icon, self.back_inv_icon_rect)
        # Vẽ các slot
        for slot in self.inventory_slots:
            pygame.draw.rect(self.screen, (80, 80, 80), slot, 2)
            mouse_pos = pygame.mouse.get_pos()
        # Lấy dữ liệu inventory từ GameState (ví dụ: {"carrot_seed": 23, ...})
        inv_dict = self.game_state.player.inventory.items
        # items = sorted(inv_dict.items())  # Sắp xếp theo key (có thể thay đổi thứ tự theo ý bạn)
        items = list(inv_dict.items())
        slot_index = 0
        for item, count in items:
            # Kiểm tra nếu count là kiểu int (để bỏ qua các mục như "rods_owned" nếu là list)
            if isinstance(count, int) and slot_index < len(self.inventory_slots):
                slot = self.inventory_slots[slot_index]
                # Vẽ icon nếu có
                if item in self.item_icons:
                    icon_img = self.item_icons[item]
                    icon_x = slot.x + (slot.width - icon_img.get_width()) // 2
                    icon_y = slot.y + (slot.height - icon_img.get_height()) // 2
                    self.screen.blit(icon_img, (icon_x, icon_y))
                # Vẽ số lượng (bao gồm cả khi bằng 0)
                count_text = self.font.render(str(count), True, WHITE)
                self.screen.blit(count_text, (slot.x + slot.width - count_text.get_width() - 2,
                                              slot.y + slot.height - count_text.get_height() - 2))
                if slot.collidepoint(mouse_pos):
                    tooltip_text = self.font.render(item, True, WHITE)
                    # Vẽ tooltip phía trên slot (với một chút padding)
                    tooltip_x = slot.x
                    tooltip_y = slot.y - tooltip_text.get_height() - 4
                    # Vẽ background cho tooltip
                    tooltip_bg = pygame.Surface((tooltip_text.get_width() + 4, tooltip_text.get_height() + 4))
                    tooltip_bg.fill((0, 0, 0))
                    self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
                    self.screen.blit(tooltip_text, (tooltip_x + 2, tooltip_y + 2))
                slot_index += 1

    def draw(self):
        # Vẽ icon UI: Settings, Map, Inventory
        self.screen.blit(self.icon_settings, self.icon_settings_rect)
        self.screen.blit(self.icon_map, self.icon_map_rect)
        self.screen.blit(self.icon_inventory, self.icon_inventory_rect)

        # Vẽ menu Settings nếu mở
        if self.show_menu:
            pygame.draw.rect(self.screen, (50, 50, 50),
                             (self.menu_x, self.menu_y, self.menu_width, self.menu_height))
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 3)
            for i, button in enumerate(self.buttons):
                button_x = self.menu_x + (self.menu_width - self.button_width) // 2
                button_y = self.menu_y + 20 + i * (self.button_height + 10)
                button["rect"].topleft = (button_x, button_y)
                color = (150, 150, 150) if button["rect"].collidepoint(pygame.mouse.get_pos()) else (100, 100, 100)
                pygame.draw.rect(self.screen, color, button["rect"])
                pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2)
                text_surface = self.font.render(button["text"], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button["rect"].center)
                self.screen.blit(text_surface, text_rect)

        # Vẽ popup Map nếu mở
        if self.show_map:
            border_x = self.map_x - 4
            border_y = self.map_y - 4
            border_w = self.map_width + 8
            border_h = self.map_height + 8
            pygame.draw.rect(self.screen, (155, 173, 183),
                             (border_x, border_y, border_w, border_h), width=4)
            pygame.draw.rect(self.screen, (50, 50, 50),
                             (self.map_x, self.map_y, self.map_width, self.map_height))
            self.screen.blit(self.map_image, (self.map_x, self.map_y))
            self.back_icon_rect = self.back_icon.get_rect(topright=(self.map_x + self.map_width - 10, self.map_y + 10))
            self.screen.blit(self.back_icon, self.back_icon_rect)

            # Tính toán vùng ngôi làng, ao cá và nông trại trên map
            village_rect = pygame.Rect(
                self.map_x + self.village_rect_rel.x,
                self.map_y + self.village_rect_rel.y,
                self.village_rect_rel.width,
                self.village_rect_rel.height
            )
            fish_rect = pygame.Rect(
                self.map_x + self.fish_rect_rel.x,
                self.map_y + self.fish_rect_rel.y,
                self.fish_rect_rel.width,
                self.fish_rect_rel.height
            )
            farm_rect = pygame.Rect(
                self.map_x + self.farm_rect_rel.x,
                self.map_y + self.farm_rect_rel.y,
                self.farm_rect_rel.width,
                self.farm_rect_rel.height
            )

            mouse_pos = pygame.mouse.get_pos()
            if village_rect.collidepoint(mouse_pos) or fish_rect.collidepoint(mouse_pos) or farm_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            # (Tuỳ chọn: vẽ viền debug)
            # pygame.draw.rect(self.screen, (255, 0, 0), village_rect, 1)
            # pygame.draw.rect(self.screen, (0, 255, 0), fish_rect, 1)
            # pygame.draw.rect(self.screen, (0, 255, 0), farm_rect, 1)

        # Vẽ popup Inventory nếu mở
        if self.show_inventory:
            self.draw_inventory()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Nếu bấm icon Settings -> bật/tắt menu Settings
            if self.icon_settings_rect.collidepoint(event.pos):
                self.show_menu = not self.show_menu
                self.show_map = False
                self.show_inventory = False
                return True
            # Nếu bấm icon Map -> bật/tắt popup Map
            if self.icon_map_rect.collidepoint(event.pos):
                self.show_map = not self.show_map
                self.show_menu = False
                self.show_inventory = False
                return True
            # Nếu bấm icon Inventory -> bật/tắt popup Inventory
            if self.icon_inventory_rect.collidepoint(event.pos):
                self.show_inventory = not self.show_inventory
                self.show_menu = False
                self.show_map = False
                return True
            # Nếu popup Map mở, xử lý event của Map
            if self.show_map:
                if self.back_icon_rect.collidepoint(event.pos):
                    self.show_map = False
                    return True
                village_rect = pygame.Rect(
                    self.map_x + self.village_rect_rel.x,
                    self.map_y + self.village_rect_rel.y,
                    self.village_rect_rel.width,
                    self.village_rect_rel.height
                )
                if village_rect.collidepoint(event.pos):
                    print("Chuyển sang giao diện Làng!")
                    self.on_village_click()
                    return True
                fish_rect = pygame.Rect(
                    self.map_x + self.fish_rect_rel.x,
                    self.map_y + self.fish_rect_rel.y,
                    self.fish_rect_rel.width,
                    self.fish_rect_rel.height
                )
                if fish_rect.collidepoint(event.pos):
                    print("Chuyển sang giao diện Câu Cá!")
                    self.on_fish_click()
                    return True
                farm_rect = pygame.Rect(
                    self.map_x + self.farm_rect_rel.x,
                    self.map_y + self.farm_rect_rel.y,
                    self.farm_rect_rel.width,
                    self.farm_rect_rel.height
                )
                if farm_rect.collidepoint(event.pos):
                    print("Chuyển sang giao diện Farm!")
                    self.on_farm_click()
                    return True
                return True
            # Nếu popup Inventory mở, xử lý event cho Inventory
            if self.show_inventory:
                if self.back_inv_icon_rect.collidepoint(event.pos):
                    self.show_inventory = False
                    return True
                for index, slot in enumerate(self.inventory_slots):
                    if slot.collidepoint(event.pos):
                        # Lấy danh sách các mục trong inventory theo thứ tự (sorted theo key)
                        items = list(self.game_state.player.inventory.items.items())
                        if index < len(items):
                            item, count = items[index]
                            # Ví dụ: nếu click vào "energy_herb", tăng năng lượng
                            if item == "energy_herb" and count > 0:
                                if(self.game_state.player.energy < 100):
                                    self.game_state.player.energy += 20  # Tăng 20 năng lượng (điều chỉnh theo nhu cầu)
                                    if(self.game_state.player.energy > 100):
                                        self.game_state.player.energy = 100
                                    self.game_state.player.inventory.remove_item("energy_herb", 1)
                                    print("Đã sử dụng Energy Herb, tăng năng lượng!")
                                    self.save_game_ui()
                                else:
                                    print("Đã đầy năng lượng")
                            # Bạn có thể mở rộng cho các loại item khác nếu cần
                            elif item == "basic_rod" and count > 0:
                                self.game_state.player.rod_level = "wood"
                                print("Đã sử dụng cần câu cơ bản")
                                self.save_game_ui()
                            elif item == "silver_rod" and count > 0:
                                self.game_state.player.rod_level = "silver"
                                print("Đã sử dụng cần câu bạc")
                                self.save_game_ui()
                            elif item == "gold_rod" and count > 0:
                                self.game_state.player.rod_level = "gold"
                                print("Đã sử dụng cần câu vàng")
                                self.save_game_ui()
                            elif item == "diamond_rod" and count > 0:
                                self.game_state.player.rod_level = "diamond"
                                print("Đã sử dụng cần câu kim cương")
                                self.save_game_ui()

                            else:
                                print("click!")
                        return True
                # Xử lý click vào các slot (có thể mở rộng chức năng)
                return True
            # Nếu menu Settings mở, xử lý các nút
            if self.show_menu:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()
                        return True
        return False

    def go_to_village_scene(self):
        print("Yêu cầu chuyển sang giao diện Làng!")
        self.running = False
        from src.scenes.village import VillageScene
        village_scene = VillageScene(self.game_state, self.screen, self)
        village_scene.run()

    def go_to_fishing_scene(self):
        print("Yêu cầu chuyển sang giao diện Câu Cá!")
        self.running = False
        from src.scenes.fishing import FishingScene
        fishing_scene = FishingScene(self.game_state, self.screen, self)
        fishing_scene.run()

    def go_to_farm_scene(self):
        print("Yêu cầu chuyển sang giao diện Farm!")
        self.running = False
        from src.scenes.farm import FarmScene
        farm_scene = FarmScene(self.game_state, self.screen, self)
        farm_scene.run()

    def save_game_ui(self):
        self.game_state.save_game()
        print("Game đã được lưu từ UI!")
        self.show_menu = False

    def main_menu_ui(self):
        print("Quay về Main Menu...")
        self.show_menu = False

    def exit_game(self):
        print("Thoát game!")
        pygame.quit()
        sys.exit()

def start_ui(game_state):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("UI Settings")
    settings_ui = SettingsUI(screen, game_state)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                settings_ui = SettingsUI(screen, game_state)
            settings_ui.handle_event(event)

        screen.fill((0, 0, 0))
        settings_ui.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    from src.core.game_state import GameState
    game_state = GameState()
    start_ui(game_state)
