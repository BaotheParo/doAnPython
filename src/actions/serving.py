import pygame
import random
import asyncio
import platform
import os
import sys

# Thiết lập BASE_DIR
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Khởi tạo Pygame
pygame.init()

# Thiết lập cửa sổ trò chơi
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Serving Minigame")
FPS = 60

# Tải hình ảnh với kiểm tra lỗi
def load_image(path, default_size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except FileNotFoundError:
        print(f"Error: File not found - {path}")
        default_img = pygame.Surface(default_size)
        default_img.fill((150, 150, 150))
        return default_img

# Tải background
background_path = os.path.join(BASE_DIR, "assets", "images", "backgrounds", "quayruou.png")
background = load_image(background_path, (SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Tải các hình ảnh thức uống
drink_paths = [
    os.path.join(BASE_DIR, "assets", "images", "drinks", "bia.png"),
    os.path.join(BASE_DIR, "assets", "images", "drinks", "nuoccam.png"),
    os.path.join(BASE_DIR, "assets", "images", "drinks", "nuocchanh.png"),
    os.path.join(BASE_DIR, "assets", "images", "drinks", "nuoctao.png"),
    os.path.join(BASE_DIR, "assets", "images", "drinks", "socola.png")
]

# Tỷ lệ gốc của các hình ảnh thức uống
drink_original_sizes = [
    (252, 252),  # bia.png
    (179, 291),  # nuoccam.png
    (252, 252),  # nuocchanh.png
    (143, 213),  # nuoctao.png
    (283, 284)   # socola.png
]

# Tải và scale hình ảnh thức uống sao cho đồng đều
drink_images = []
UNIFORM_SIZE = (120, 120)  # Kích thước đồng nhất cho tất cả hình ảnh thức uống
for path, original_size in zip(drink_paths, drink_original_sizes):
    img = load_image(path, UNIFORM_SIZE)
    scale_ratio = min(UNIFORM_SIZE[0] / original_size[0], UNIFORM_SIZE[1] / original_size[1])
    scaled_width = int(original_size[0] * scale_ratio)
    scaled_height = int(original_size[1] * scale_ratio)
    img = pygame.transform.scale(img, (scaled_width, scaled_height))
    uniform_img = pygame.Surface(UNIFORM_SIZE, pygame.SRCALPHA)
    img_x = (UNIFORM_SIZE[0] - scaled_width) // 2
    img_y = (UNIFORM_SIZE[1] - scaled_height) // 2
    uniform_img.blit(img, (img_x, img_y))
    drink_images.append(uniform_img)

# Tải các hình ảnh nhân vật
char_paths = [
    os.path.join(BASE_DIR, "assets", "images", "characters", "nhanvat1.png"),
    os.path.join(BASE_DIR, "assets", "images", "characters", "nhanvat2.png"),
    os.path.join(BASE_DIR, "assets", "images", "characters", "nhanvat3.png")
]
character_images = [load_image(path, (120, 120)) for path in char_paths]
character_images = [pygame.transform.scale(img, (120, 120)) for img in character_images]

# Tải khung pixel art
frame_path = os.path.join(BASE_DIR, "assets", "images", "icons", "frame.png")
khungnuoc_path = os.path.join(BASE_DIR, "assets", "images", "icons", "khungnuoc.png")
current_drink_frame_img = load_image(frame_path, (200, 200))
current_drink_frame_img = pygame.transform.scale(current_drink_frame_img, (200, 200))
speech_frame_img = load_image(khungnuoc_path, (120, 100))
speech_frame_img = pygame.transform.scale(speech_frame_img, (120, 100))

# Font pixel
font_path = os.path.join(BASE_DIR, "assets", "fonts", "pixel_font.ttf")
font = pygame.font.Font(font_path, 36) if os.path.exists(font_path) else pygame.font.Font(None, 36)
small_font = pygame.font.Font(font_path, 18) if os.path.exists(font_path) else pygame.font.Font(None, 18)

# Thiết lập vị trí
DRINK_POSITIONS = [(318, 612), (488, 612), (658, 612), (828, 612), (998, 612)]
CUSTOMER_POSITIONS = [
    (83, 380), (229, 380), (375, 380), (521, 380),
    (667, 380), (813, 380), (959, 380), (1105, 380)
]

# Kích thước
DRINK_RECT_SIZE = (120, 120)
CUSTOMER_RECT_SIZE = (120, 120)
SPEECH_FRAME_SIZE = (120, 100)
DRINK_IN_SPEECH_SIZE_DEFAULT = (100, 100)
CURRENT_DRINK_FRAME_POS = (585, 0)
CURRENT_DRINK_FRAME_SIZE = (200, 200)
CURRENT_DRINK_IMAGE_SIZE = (180, 180)  # Giảm xuống để vừa khung

# Kích thước tùy chỉnh cho speech drink
DRINK_IN_SPEECH_SIZES = [
    (100, 100),  # bia.png
    (500, 90),   # nuoccam.png
    (100, 100),  # nuocchanh.png
    (120, 100),  # nuoctao.png
    (100, 100)   # socola.png
]

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

class Drink:
    def __init__(self, image, position, drink_type):
        self.image = image
        self.position = position
        self.rect = pygame.Rect(position[0] - DRINK_RECT_SIZE[0] // 2, position[1] - DRINK_RECT_SIZE[1] // 2, DRINK_RECT_SIZE[0], DRINK_RECT_SIZE[1])
        self.drink_type = drink_type
        self.image_pos = (
            position[0] - UNIFORM_SIZE[0] // 2,
            position[1] - UNIFORM_SIZE[1] // 2
        )

    def draw(self, screen):
        screen.blit(self.image, self.image_pos)

class Customer:
    def __init__(self, image, position, drink_type):
        self.image = image
        self.position = position
        self.rect = pygame.Rect(position[0] - CUSTOMER_RECT_SIZE[0] // 2, position[1] - CUSTOMER_RECT_SIZE[1] // 2, CUSTOMER_RECT_SIZE[0], CUSTOMER_RECT_SIZE[1])
        self.drink_type = drink_type
        self.timer = 2.5
        self.speech_frame_rect = pygame.Rect(position[0] - SPEECH_FRAME_SIZE[0] // 2, position[1] - SPEECH_FRAME_SIZE[1] - 55, SPEECH_FRAME_SIZE[0], SPEECH_FRAME_SIZE[1])
        drink_size = DRINK_IN_SPEECH_SIZES[self.drink_type]
        original_size = drink_original_sizes[self.drink_type]
        scale_ratio = min(drink_size[0] / original_size[0], drink_size[1] / original_size[1])
        scaled_width = int(original_size[0] * scale_ratio)
        scaled_height = int(original_size[1] * scale_ratio)
        temp_img = pygame.transform.scale(drink_images[self.drink_type], (scaled_width, scaled_height))
        self.drink_image = pygame.Surface(drink_size, pygame.SRCALPHA)
        img_x = (drink_size[0] - scaled_width) // 2
        img_y = (drink_size[1] - scaled_height) // 2
        self.drink_image.blit(temp_img, (img_x, img_y))
        self.drink_in_speech_rect = self.drink_image.get_rect(center=self.speech_frame_rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(speech_frame_img, self.speech_frame_rect)
        screen.blit(self.drink_image, self.drink_in_speech_rect)

    def update(self, dt):
        self.timer -= dt
        return self.timer <= 0

class ServingMinigame:
    def __init__(self):
        self.background = background
        self.drinks = []
        self.customers = []
        self.score = 0
        self.game_time = 30.0
        self.countdown_time = 3.0
        self.state = 'start'
        self.customer_spawn_timer = 0.0
        self.customer_spawn_interval = 1.0
        self.max_customers = 5
        self.available_positions = list(range(8))
        self.current_drink = None
        self.current_drink_image = None
        self.current_drink_frame = pygame.Rect(CURRENT_DRINK_FRAME_POS[0], CURRENT_DRINK_FRAME_POS[1], CURRENT_DRINK_FRAME_SIZE[0], CURRENT_DRINK_FRAME_SIZE[1])
        self.current_drink_image_rect = pygame.Rect(
            CURRENT_DRINK_FRAME_POS[0] + (CURRENT_DRINK_FRAME_SIZE[0] - CURRENT_DRINK_IMAGE_SIZE[0]) // 2,
            CURRENT_DRINK_FRAME_POS[1] + (CURRENT_DRINK_FRAME_SIZE[1] - CURRENT_DRINK_IMAGE_SIZE[1]) // 2,
            CURRENT_DRINK_IMAGE_SIZE[0], CURRENT_DRINK_IMAGE_SIZE[1]
        )
        self.blink_timer = 0.0
        self.setup_drinks()

    def setup_drinks(self):
        drink_types = list(range(5))
        random.shuffle(drink_types)
        self.drinks = [Drink(drink_images[drink_types[i]], pos, drink_types[i]) for i, pos in enumerate(DRINK_POSITIONS)]

    def spawn_customer(self):
        if len(self.available_positions) == 0 or len(self.customers) >= self.max_customers:
            return
        position_index = random.choice(self.available_positions)
        self.available_positions.remove(position_index)
        position = CUSTOMER_POSITIONS[position_index]
        character_image = random.choice(character_images)
        drink_type = random.randint(0, 4)
        customer = Customer(character_image, position, drink_type)
        self.customers.append(customer)

    def update(self, dt):
        if self.state == 'playing':
            self.game_time -= dt
            self.blink_timer += dt
            if self.game_time <= 0:
                self.state = 'result'
                return

            self.customer_spawn_interval = 0.5 if self.game_time <= 8 else 0.8 if self.game_time <= 20 else 1.0
            self.customer_spawn_timer -= dt
            if self.customer_spawn_timer <= 0:
                self.spawn_customer()
                self.customer_spawn_timer = self.customer_spawn_interval

            for customer in self.customers[:]:
                if customer.update(dt):
                    self.customers.remove(customer)
                    self.available_positions.append(CUSTOMER_POSITIONS.index(customer.position))

        elif self.state == 'countdown':
            self.countdown_time -= dt
            if self.countdown_time <= 0:
                self.state = 'playing'
                self.game_time = 30.0
                self.customer_spawn_timer = 0.0

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if self.state == 'start':
            text = font.render("Do you want to play game?", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
            pygame.draw.rect(screen, GREEN, start_button)
            text = font.render("Start Game", True, BLACK)
            screen.blit(text, (start_button.x + (start_button.width - text.get_width()) // 2, start_button.y + (start_button.height - text.get_height()) // 2))
        elif self.state == 'countdown':
            text = font.render(str(int(self.countdown_time) + 1), True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        elif self.state == 'playing':
            for customer in self.customers:
                customer.draw(screen)
            for drink in self.drinks:
                drink.draw(screen)
            screen.blit(current_drink_frame_img, self.current_drink_frame)
            if self.current_drink_image:
                if int(self.blink_timer * 4) % 2 == 0:
                    screen.blit(self.current_drink_image, self.current_drink_image_rect)
            time_text = font.render(f"Time: {self.game_time:.1f}", True, WHITE)
            score_text = font.render(f"Point: {self.score}", True, WHITE)
            screen.blit(time_text, (10, 10))
            screen.blit(score_text, (10, 50))
            mouse_pos = pygame.mouse.get_pos()
            mouse_coord_text = small_font.render(f"Mouse: ({mouse_pos[0]},{mouse_pos[1]})", True, WHITE)
            screen.blit(mouse_coord_text, (10, 70))
        elif self.state == 'result':
            text = font.render(f"Your point: {self.score}", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
            pygame.draw.rect(screen, GREEN, play_again_button)
            text = font.render("Play Again", True, BLACK)
            screen.blit(text, (play_again_button.x + (play_again_button.width - text.get_width()) // 2, play_again_button.y + (play_again_button.height - text.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.state == 'start':
                start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
                if start_button.collidepoint(mouse_pos):
                    self.state = 'countdown'
                    self.countdown_time = 3.0
            elif self.state == 'playing':
                for drink in self.drinks:
                    if drink.rect.collidepoint(mouse_pos):
                        self.current_drink = drink.drink_type
                        self.current_drink_image = drink_images[drink.drink_type]
                        self.blink_timer = 0.0
                        break
                for customer in self.customers[:]:
                    if customer.drink_in_speech_rect.collidepoint(mouse_pos) and self.current_drink is not None:
                        if customer.drink_type == self.current_drink:
                            self.score += 1
                        self.customers.remove(customer)
                        self.available_positions.append(CUSTOMER_POSITIONS.index(customer.position))
                        break
            elif self.state == 'result':
                play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
                if play_again_button.collidepoint(mouse_pos):
                    self.current_drink = None
                    self.current_drink_image = None
                    self.__init__()

def setup():
    global game
    game = ServingMinigame()

def update_loop():
    global game
    dt = 1.0 / FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return
        game.handle_event(event)
    game.update(dt)
    game.draw(screen)
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())