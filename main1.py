import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Village Adventure")
clock = pygame.time.Clock()

# Cấu hình tile
TILE_SIZE = 32
MAP_WIDTH = 120
MAP_HEIGHT = 120

# Định nghĩa các loại tile
TILE_TYPES = {
    "G": {"name": "grass", "collidable": False},   # Cỏ
    "T": {"name": "tree", "collidable": True},     # Cây
    "W": {"name": "water", "collidable": True},    # Nước
    "D": {"name": "dirt", "collidable": False},    # Đất
    "H": {"name": "house", "collidable": True},    # Nhà (2x2 tile)
    "F": {"name": "fence", "collidable": True},    # Hàng rào
    "C": {"name": "crate", "collidable": True},    # Thùng gỗ
    "B": {"name": "bridge", "collidable": False},  # Cầu
    "P1": {"name": "plant_wheat", "collidable": False},  # Lúa (giai đoạn 1)
    "P2": {"name": "plant_carrot", "collidable": False}, # Cà rốt (giai đoạn 1)
    "P3": {"name": "plant_pumpkin", "collidable": False},# Bí ngô (giai đoạn 1)
    "P4": {"name": "plant_wheat_mature", "collidable": False},  # Lúa trưởng thành
    "P5": {"name": "plant_carrot_mature", "collidable": False}, # Cà rốt trưởng thành
    "P6": {"name": "plant_pumpkin_mature", "collidable": False},# Bí ngô trưởng thành
}

# Tạo bản đồ
game_map = [["G" for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

# Thêm sông (rộng 4 tile)
river_y_start = MAP_HEIGHT // 2 - 2
for y in range(river_y_start, river_y_start + 4):
    for x in range(MAP_WIDTH):
        if 0 <= y < MAP_HEIGHT:
            game_map[y][x] = "W"
# Cây cầu
bridge_x = MAP_WIDTH // 2
for y in range(river_y_start, river_y_start + 4):
    game_map[y][bridge_x] = "B"
    game_map[y][bridge_x + 1] = "B"
    game_map[y][bridge_x + 2] = "B"

# Thêm các con đường chính (đất)
village_center_x, village_center_y = MAP_WIDTH // 2, river_y_start - 10
for x in range(village_center_x - 20, village_center_x + 20):
    game_map[village_center_y][x] = "D"
    game_map[village_center_y + 8][x] = "D"
    game_map[village_center_y - 8][x] = "D"
for y in range(village_center_y - 15, village_center_y + 15):
    game_map[y][village_center_x - 8] = "D"
    game_map[y][village_center_x + 8] = "D"
for y in range(village_center_y + 15, river_y_start):
    game_map[y][bridge_x] = "D"
    game_map[y][bridge_x + 1] = "D"
    game_map[y][bridge_x + 2] = "D"

# Thêm khu trồng trọt (10x10 tile, gần làng)
farm_x, farm_y = village_center_x + 12, village_center_y - 5
for y in range(farm_y, farm_y + 10):
    for x in range(farm_x, farm_x + 10):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            game_map[y][x] = "D"

# Thêm khu vực chuồng trại (10x10 tile, phía tây làng)
barn_x, barn_y = village_center_x - 22, village_center_y - 5
for y in range(barn_y, barn_y + 10):
    for x in range(barn_x, barn_x + 10):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            game_map[y][x] = "D"
for y in [barn_y, barn_y + 9]:
    for x in range(barn_x, barn_x + 10):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            game_map[y][x] = "F"
for x in [barn_x, barn_x + 9]:
    for y in range(barn_y, barn_y + 10):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            game_map[y][x] = "F"

# Thêm khu vực làng (30x30 tile)
for y in range(village_center_y - 15, village_center_y + 15):
    for x in range(village_center_x - 15, village_center_x + 15):
        if 0 <= x < MAP_WIDTH - 1 and 0 <= y < MAP_HEIGHT - 1:
            if game_map[y][x] != "D" and random.random() < 0.05:
                game_map[y][x] = "H"
                game_map[y][x+1] = "H"
                game_map[y+1][x] = "H"
                game_map[y+1][x+1] = "H"
            elif game_map[y][x] != "D" and random.random() < 0.05:
                game_map[y][x] = "F"
            elif game_map[y][x] != "D" and random.random() < 0.05:
                game_map[y][x] = "C"
            elif game_map[y][x] != "D" and random.random() < 0.07:
                game_map[y][x] = "T"

# Nhân vật người chơi
player_size = 24
player_pos = pygame.Vector2(village_center_x * TILE_SIZE, village_center_y * TILE_SIZE)
player_speed = 4
player_frame = 0
player_direction = "down"
animation_timer = 0
ANIMATION_SPEED = 10

# Thú cưng của người chơi (chó sói)
player_pet = {
    "pos": pygame.Vector2(player_pos.x - 32, player_pos.y),
    "size": 16,
    "direction": "down",
    "frame": 0,
    "animation_timer": 0
}

# Tạo danh sách NPC
NPC_COUNT = 12
npcs = []
for _ in range(NPC_COUNT):
    while True:
        x = random.randint(village_center_x - 15, village_center_x + 14) * TILE_SIZE
        y = random.randint(village_center_y - 15, village_center_y + 14) * TILE_SIZE
        tile_x, tile_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
        if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
            if not TILE_TYPES[game_map[tile_y][tile_x]]["collidable"]:
                npc = {
                    "pos": pygame.Vector2(x, y),
                    "size": 24,
                    "task": None,
                    "target": None,
                    "action_timer": 0,
                    "direction": "down",
                    "frame": 0,
                    "animation_timer": 0
                }
                pet = {
                    "pos": pygame.Vector2(x - 32, y),
                    "size": 16,
                    "direction": "down",
                    "frame": 0,
                    "animation_timer": 0
                }
                npc["pet"] = pet
                npcs.append(npc)
                break

# Tạo danh sách gia súc
ANIMAL_COUNT = 10
animals = []
for _ in range(ANIMAL_COUNT):
    while True:
        x = random.randint(barn_x + 1, barn_x + 8) * TILE_SIZE
        y = random.randint(barn_y + 1, barn_y + 8) * TILE_SIZE
        tile_x, tile_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
        if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
            if not TILE_TYPES[game_map[tile_y][tile_x]]["collidable"]:
                animals.append({
                    "pos": pygame.Vector2(x, y),
                    "size": 16,
                    "type": random.choice(["chicken", "duck", "pig"]),
                    "direction": "down",
                    "frame": 0,
                    "animation_timer": 0
                })
                break

# Hệ thống cây trồng
plant_growth_timer = 0
PLANT_GROWTH_INTERVAL = 600
mature_plants = ["P4", "P5", "P6"]
plant_types = ["P1", "P2", "P3"]

# Hệ thống đối thoại
dialogue_text = None
dialogue_timer = 0
DIALOGUE_DURATION = 120
prompt_text = None
interaction_distance = 64

# Font cho giao diện
font = pygame.font.Font(None, 28)

# Hàm vẽ sprite pixel art
def draw_tile(tile_type, x, y):
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    if tile_type == "G":
        surface.fill((60, 180, 60))
        for _ in range(12):
            px = random.randint(2, TILE_SIZE-2)
            py = random.randint(2, TILE_SIZE-2)
            pygame.draw.rect(surface, (40, 150, 40), (px, py, 2, 2))
        for _ in range(4):
            px = random.randint(4, TILE_SIZE-4)
            py = random.randint(4, TILE_SIZE-4)
            pygame.draw.rect(surface, (255, 200, 200), (px, py, 2, 2))
    
    elif tile_type == "T":
        draw_tile("G", 0, 0)
        pygame.draw.rect(surface, (80, 40, 10), (TILE_SIZE//2-5, 12, 10, 20))
        pygame.draw.rect(surface, (100, 60, 20), (TILE_SIZE//2-4, 13, 8, 18))
        pygame.draw.circle(surface, (0, 100, 0), (TILE_SIZE//2, 8), 15)
        pygame.draw.circle(surface, (0, 120, 0), (TILE_SIZE//2, 8), 13)
        pygame.draw.circle(surface, (0, 140, 0), (TILE_SIZE//2-3, 6), 9)
    
    elif tile_type == "W":
        surface.fill((20, 100, 220))
        for i in range(5):
            px = random.randint(4, TILE_SIZE-12)
            py = 4 + i * 6
            pygame.draw.rect(surface, (60, 140, 255), (px, py, 12, 3))
        pygame.draw.rect(surface, (255, 255, 255, 80), (0, 0, TILE_SIZE, 8))
        if y // TILE_SIZE > 0 and game_map[y // TILE_SIZE - 1][x // TILE_SIZE] != "W":
            pygame.draw.rect(surface, (40, 150, 40), (0, 0, TILE_SIZE, 10))
    
    elif tile_type == "D":
        surface.fill((160, 100, 60))
        for _ in range(10):
            px = random.randint(2, TILE_SIZE-2)
            py = random.randint(2, TILE_SIZE-2)
            pygame.draw.rect(surface, (130, 80, 40), (px, py, 2, 2))
        for _ in range(4):
            px = random.randint(4, TILE_SIZE-4)
            py = random.randint(4, TILE_SIZE-4)
            pygame.draw.rect(surface, (100, 100, 100), (px, py, 3, 3))
    
    elif tile_type == "H":
        surface.fill((60, 180, 60))
        pygame.draw.rect(surface, (90, 90, 90), (2, 6, TILE_SIZE*2-4, TILE_SIZE*2-12))
        pygame.draw.rect(surface, (120, 120, 120), (3, 7, TILE_SIZE*2-6, TILE_SIZE*2-14))
        pygame.draw.polygon(surface, (210, 60, 60), [(2, 6), (TILE_SIZE, -2), (TILE_SIZE*2-2, 6)])
        pygame.draw.polygon(surface, (230, 80, 80), [(3, 5), (TILE_SIZE, 0), (TILE_SIZE*2-3, 5)])
        if x % (2*TILE_SIZE) == 0 and y % (2*TILE_SIZE) == TILE_SIZE:
            pygame.draw.rect(surface, (80, 40, 10), (TILE_SIZE//2-4, TILE_SIZE-16, 16, 16))
            pygame.draw.rect(surface, (100, 60, 20), (TILE_SIZE//2-3, TILE_SIZE-15, 14, 14))
            pygame.draw.rect(surface, (60, 30, 0), (TILE_SIZE//2+4, TILE_SIZE-15, 2, 14))
        if x % (2*TILE_SIZE) == TILE_SIZE and y % (2*TILE_SIZE) == 0:
            pygame.draw.rect(surface, (140, 200, 255), (6, 10, 12, 12))
            pygame.draw.rect(surface, (160, 220, 255), (7, 11, 10, 10))
            pygame.draw.rect(surface, (100, 100, 100), (11, 10, 2, 12))
    
    elif tile_type == "F":
        draw_tile("G", 0, 0)
        pygame.draw.rect(surface, (90, 50, 10), (TILE_SIZE//2-6, 6, 12, 22))
        pygame.draw.rect(surface, (110, 70, 30), (TILE_SIZE//2-5, 7, 10, 20))
        pygame.draw.rect(surface, (80, 40, 0), (TILE_SIZE//2-8, 10, 16, 4))
    
    elif tile_type == "C":
        draw_tile("G", 0, 0)
        pygame.draw.rect(surface, (90, 50, 10), (6, 6, 20, 20))
        pygame.draw.rect(surface, (110, 70, 30), (7, 7, 18, 18))
        pygame.draw.rect(surface, (80, 40, 0), (7, 12, 18, 3))
        pygame.draw.rect(surface, (80, 40, 0), (12, 7, 3, 18))
    
    elif tile_type == "B":
        surface.fill((140, 90, 50))
        pygame.draw.rect(surface, (160, 110, 70), (2, 0, TILE_SIZE-4, TILE_SIZE))
        for i in range(0, TILE_SIZE, 4):
            pygame.draw.rect(surface, (120, 70, 30), (2, i, TILE_SIZE-4, 3))
        pygame.draw.rect(surface, (90, 50, 10), (0, 0, 4, TILE_SIZE))
        pygame.draw.rect(surface, (90, 50, 10), (TILE_SIZE-4, 0, 4, TILE_SIZE))
    
    elif tile_type == "P1":
        draw_tile("D", 0, 0)
        pygame.draw.rect(surface, (0, 120, 0), (TILE_SIZE//2-2, 24, 4, 8))
    
    elif tile_type == "P2":
        draw_tile("D", 0, 0)
        pygame.draw.rect(surface, (0, 100, 0), (TILE_SIZE//2-3, 24, 6, 8))
    
    elif tile_type == "P3":
        draw_tile("D", 0, 0)
        pygame.draw.rect(surface, (0, 110, 0), (TILE_SIZE//2-4, 22, 8, 10))
    
    elif tile_type == "P4":
        draw_tile("D", 0, 0)
        pygame.draw.rect(surface, (200, 180, 50), (TILE_SIZE//2-4, 16, 8, 16))
        pygame.draw.rect(surface, (220, 200, 70), (TILE_SIZE//2-3, 17, 6, 14))
        pygame.draw.rect(surface, (180, 160, 40), (TILE_SIZE//2-5, 20, 10, 4))
    
    elif tile_type == "P5":
        draw_tile("D", 0, 0)
        pygame.draw.rect(surface, (0, 120, 0), (TILE_SIZE//2-4, 20, 8, 12))
        pygame.draw.rect(surface, (255, 140, 0), (TILE_SIZE//2-2, 24, 4, 8))
    
    elif tile_type == "P6":
        draw_tile("D", 0, 0)
        pygame.draw.rect(surface, (0, 120, 0), (TILE_SIZE//2-6, 18, 12, 14))
        pygame.draw.circle(surface, (255, 160, 0), (TILE_SIZE//2, 24), 6)
    
    screen.blit(surface, (x, y))

# Hàm vẽ nhân vật
def draw_character(surface, pos_x, pos_y, size, is_player=False, direction="down", frame=0):
    body_color = (80, 160, 240) if is_player else (240, 120, 120)
    pygame.draw.rect(surface, (60, 60, 60), (pos_x+2, pos_y+10, size-4, size-12))
    pygame.draw.rect(surface, body_color, (pos_x+3, pos_y+11, size-6, size-14))
    pygame.draw.rect(surface, (200, 160, 120), (pos_x+size//4, pos_y+2, size//2, size//2))
    hair_color = (110, 80, 60) if is_player else (60, 110, 60)
    if direction == "up":
        pygame.draw.rect(surface, hair_color, (pos_x+size//4, pos_y, size//2, 6))
        pygame.draw.rect(surface, hair_color, (pos_x+size//4-2, pos_y+2, size//2+4, 3))
    elif direction == "down":
        pygame.draw.rect(surface, hair_color, (pos_x+size//4, pos_y+2, size//2, 6))
    else:
        pygame.draw.rect(surface, hair_color, (pos_x+size//4, pos_y+1, size//2, 5))
        pygame.draw.rect(surface, hair_color, (pos_x+size//4-2, pos_y+3, size//2+4, 3))
    eye_x = pos_x + size//4 + 4
    eye_y = pos_y + 10
    pygame.draw.rect(surface, (0, 0, 0), (eye_x, eye_y, 2, 2))
    pygame.draw.rect(surface, (0, 0, 0), (eye_x + size//4-2, eye_y, 2, 2))
    if is_player or frame >= 0:
        if direction == "left" or direction == "right":
            leg_offset = 3 if frame % 2 == 0 else -3
            pygame.draw.rect(surface, (60, 60, 60), (pos_x+3, pos_y+size-8, 5, 8))
            pygame.draw.rect(surface, (60, 60, 60), (pos_x+size-8, pos_y+size-8+leg_offset, 5, 8))
        else:
            leg_offset = 3 if frame % 2 == 0 else 0
            pygame.draw.rect(surface, (60, 60, 60), (pos_x+3, pos_y+size-8+leg_offset, 5, 8))
            pygame.draw.rect(surface, (60, 60, 60), (pos_x+size-8, pos_y+size-8, 5, 8))

# Hàm vẽ thú cưng (chó sói) hoặc gia súc
def draw_animal(surface, pos_x, pos_y, size, animal_type="wolf", direction="down", frame=0):
    if animal_type == "wolf":
        body_color = (100, 100, 100)
        pygame.draw.rect(surface, body_color, (pos_x+2, pos_y+4, size-4, size-4))
        pygame.draw.rect(surface, (120, 120, 120), (pos_x+3, pos_y+5, size-6, size-6))
        pygame.draw.rect(surface, body_color, (pos_x+size-4, pos_y+2, 4, 4))  # Đuôi
        pygame.draw.rect(surface, (80, 80, 80), (pos_x, pos_y+2, 4, 4))  # Mõm
        leg_offset = 2 if frame % 2 == 0 else -2
        pygame.draw.rect(surface, (80, 80, 80), (pos_x+2, pos_y+size-4+leg_offset, 3, 4))
        pygame.draw.rect(surface, (80, 80, 80), (pos_x+size-5, pos_y+size-4, 3, 4))
    elif animal_type == "chicken":
        body_color = (255, 255, 200)
        pygame.draw.rect(surface, body_color, (pos_x+2, pos_y+4, size-4, size-4))
        pygame.draw.rect(surface, (255, 200, 100), (pos_x+size-4, pos_y+2, 3, 3))  # Mỏ
        leg_offset = 2 if frame % 2 == 0 else -2
        pygame.draw.rect(surface, (255, 200, 100), (pos_x+3, pos_y+size-4+leg_offset, 2, 4))
        pygame.draw.rect(surface, (255, 200, 100), (pos_x+size-5, pos_y+size-4, 2, 4))
    elif animal_type == "duck":
        body_color = (200, 255, 200)
        pygame.draw.rect(surface, body_color, (pos_x+2, pos_y+4, size-4, size-4))
        pygame.draw.rect(surface, (255, 200, 100), (pos_x+size-4, pos_y+2, 3, 3))  # Mỏ
        leg_offset = 2 if frame % 2 == 0 else -2
        pygame.draw.rect(surface, (255, 200, 100), (pos_x+3, pos_y+size-4+leg_offset, 2, 4))
        pygame.draw.rect(surface, (255, 200, 100), (pos_x+size-5, pos_y+size-4, 2, 4))
    elif animal_type == "pig":
        body_color = (255, 200, 200)
        pygame.draw.rect(surface, body_color, (pos_x+2, pos_y+4, size-4, size-4))
        pygame.draw.rect(surface, (255, 220, 220), (pos_x, pos_y+2, 3, 3))  # Mũi
        leg_offset = 2 if frame % 2 == 0 else -2
        pygame.draw.rect(surface, (255, 180, 180), (pos_x+2, pos_y+size-4+leg_offset, 3, 4))
        pygame.draw.rect(surface, (255, 180, 180), (pos_x+size-5, pos_y+size-4, 3, 4))

# Hàm vẽ hiệu ứng công việc
def draw_task_effect(surface, pos_x, pos_y, task):
    if task == "plant":
        pygame.draw.rect(surface, (255, 255, 255), (pos_x + 8, pos_y - 8, 8, 8))
    elif task == "harvest":
        pygame.draw.rect(surface, (255, 255, 0), (pos_x + 8, pos_y - 8, 8, 8))
    elif task == "fish":
        pygame.draw.rect(surface, (100, 100, 100), (pos_x + 8, pos_y - 8, 12, 4))
        pygame.draw.line(surface, (255, 255, 255), (pos_x + 20, pos_y - 6), (pos_x + 30, pos_y + 10), 1)

# Hàm vẽ HUD
def draw_hud(player_pos, npcs, game_map):
    hud_surface = pygame.Surface((250, 80), pygame.SRCALPHA)
    hud_surface.fill((20, 20, 20, 200))
    coord_text = f"X: {int(player_pos.x // TILE_SIZE)} Y: {int(player_pos.y // TILE_SIZE)}"
    coord_surface = font.render(coord_text, True, (255, 255, 255))
    hud_surface.blit(coord_surface, (10, 10))
    nearby_npcs = sum(1 for npc in npcs if player_pos.distance_to(npc["pos"]) < interaction_distance)
    npc_text = f"NPCs nearby: {nearby_npcs}"
    npc_surface = font.render(npc_text, True, (255, 255, 255))
    hud_surface.blit(npc_surface, (10, 30))
    mature_count = sum(1 for y in range(MAP_HEIGHT) for x in range(MAP_WIDTH) if game_map[y][x] in mature_plants)
    plant_text = f"Mature plants: {mature_count}"
    plant_surface = font.render(plant_text, True, (255, 255, 255))
    hud_surface.blit(plant_surface, (10, 50))
    screen.blit(hud_surface, (10, 10))

# Hàm vẽ bản đồ
def draw_map(offset_x, offset_y):
    start_tile_x = max(0, offset_x // TILE_SIZE - 1)
    start_tile_y = max(0, offset_y // TILE_SIZE - 1)
    tiles_x = min(MAP_WIDTH, start_tile_x + SCREEN_WIDTH // TILE_SIZE + 2)
    tiles_y = min(MAP_HEIGHT, start_tile_y + SCREEN_HEIGHT // TILE_SIZE + 2)
    for y in range(start_tile_y, tiles_y):
        for x in range(start_tile_x, tiles_x):
            tile = game_map[y][x]
            draw_tile(tile, x * TILE_SIZE - offset_x, y * TILE_SIZE - offset_y)

# Hàm kiểm tra va chạm
def check_tile_collision(new_pos, size):
    player_rect = pygame.Rect(new_pos.x, new_pos.y, size, size)
    for y in range(max(0, int(new_pos.y // TILE_SIZE) - 1), 
                   min(MAP_HEIGHT, int((new_pos.y + size) // TILE_SIZE) + 2)):
        for x in range(max(0, int(new_pos.x // TILE_SIZE) - 1), 
                       min(MAP_WIDTH, int((new_pos.x + size) // TILE_SIZE) + 2)):
            if TILE_TYPES[game_map[y][x]]["collidable"]:
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(tile_rect):
                    return True
    return False

# Hàm kiểm tra khoảng cách đến NPC
def check_nearby_npc(player_pos, npcs):
    for npc in npcs:
        distance = player_pos.distance_to(npc["pos"])
        if distance < interaction_distance:
            return True
    return False

# Hàm kiểm tra cây trồng gần người chơi
def check_nearby_plant(player_pos, game_map):
    for y in range(max(0, int(player_pos.y // TILE_SIZE) - 2), 
                   min(MAP_HEIGHT, int(player_pos.y // TILE_SIZE) + 3)):
        for x in range(max(0, int(player_pos.x // TILE_SIZE) - 2), 
                       min(MAP_WIDTH, int(player_pos.x // TILE_SIZE) + 3)):
            if game_map[y][x] in mature_plants:
                plant_pos = pygame.Vector2(x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2)
                if player_pos.distance_to(plant_pos) < interaction_distance:
                    return (x, y)
    return None

# Hàm cập nhật thú cưng
def update_pet(pet, owner_pos, owner_direction):
    target_pos = owner_pos - pygame.Vector2(32 if owner_direction in ["left", "down"] else -32, 
                                            32 if owner_direction == "down" else -32)
    direction = target_pos - pet["pos"]
    if direction.length() > 4:
        direction = direction.normalize()
        new_pos = pet["pos"] + direction * 3
        if not check_tile_collision(new_pos, pet["size"]):
            pet["pos"] = new_pos
            pet["direction"] = owner_direction
            pet["animation_timer"] += 1
            if pet["animation_timer"] >= ANIMATION_SPEED:
                pet["frame"] = (pet["frame"] + 1) % 2
                pet["animation_timer"] = 0

# Hàm cập nhật gia súc
def update_animal(animal, barn_x, barn_y):
    if random.random() < 0.02:
        direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        if direction.length() > 0:
            direction = direction.normalize()
            new_pos = animal["pos"] + direction * 2
            tile_x, tile_y = int(new_pos.x // TILE_SIZE), int(new_pos.y // TILE_SIZE)
            if (barn_x + 1 <= tile_x <= barn_x + 8 and barn_y + 1 <= tile_y <= barn_y + 8 and
                not check_tile_collision(new_pos, animal["size"])):
                animal["pos"] = new_pos
                if abs(direction.x) > abs(direction.y):
                    animal["direction"] = "right" if direction.x > 0 else "left"
                else:
                    animal["direction"] = "down" if direction.y > 0 else "up"
                animal["animation_timer"] += 1
                if animal["animation_timer"] >= ANIMATION_SPEED:
                    animal["frame"] = (animal["frame"] + 1) % 2
                    animal["animation_timer"] = 0

# Hàm cập nhật NPC
def update_npc(npc, game_map, farm_x, farm_y, river_y_start):
    if npc["action_timer"] > 0:
        npc["action_timer"] -= 1
        return

    if not npc["task"] or random.random() < 0.05:
        npc["task"] = random.choice(["plant", "harvest", "fish"])
        npc["target"] = None

    if not npc["target"]:
        if npc["task"] == "plant":
            min_dist = float("inf")
            target = None
            for y in range(farm_y, farm_y + 10):
                for x in range(farm_x, farm_x + 10):
                    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and game_map[y][x] == "D":
                        dist = abs(npc["pos"].x - x * TILE_SIZE) + abs(npc["pos"].y - y * TILE_SIZE)
                        if dist < min_dist:
                            min_dist = dist
                            target = pygame.Vector2(x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2)
            npc["target"] = target
        elif npc["task"] == "harvest":
            min_dist = float("inf")
            target = None
            for y in range(farm_y, farm_y + 10):
                for x in range(farm_x, farm_x + 10):
                    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and game_map[y][x] in mature_plants:
                        dist = abs(npc["pos"].x - x * TILE_SIZE) + abs(npc["pos"].y - y * TILE_SIZE)
                        if dist < min_dist:
                            min_dist = dist
                            target = pygame.Vector2(x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2)
            npc["target"] = target
        elif npc["task"] == "fish":
            min_dist = float("inf")
            target = None
            for x in range(MAP_WIDTH):
                y = river_y_start - 1
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and game_map[y][x] != "W":
                    dist = abs(npc["pos"].x - x * TILE_SIZE) + abs(npc["pos"].y - y * TILE_SIZE)
                    if dist < min_dist:
                        min_dist = dist
                        target = pygame.Vector2(x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2)
            npc["target"] = target

    if npc["target"]:
        direction = npc["target"] - npc["pos"]
        if direction.length() > 4:
            direction = direction.normalize()
            new_pos = npc["pos"] + direction * 4  # Tăng tốc độ NPC
            if not check_tile_collision(new_pos, npc["size"]):
                npc["pos"] = new_pos
                if abs(direction.x) > abs(direction.y):
                    npc["direction"] = "right" if direction.x > 0 else "left"
                else:
                    npc["direction"] = "down" if direction.y > 0 else "up"
                npc["animation_timer"] += 1
                if npc["animation_timer"] >= ANIMATION_SPEED:
                    npc["frame"] = (npc["frame"] + 1) % 2
                    npc["animation_timer"] = 0
            if direction.length() < 32:
                tile_x = int(npc["target"].x // TILE_SIZE)
                tile_y = int(npc["target"].y // TILE_SIZE)
                if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                    if npc["task"] == "plant" and game_map[tile_y][tile_x] == "D":
                        game_map[tile_y][tile_x] = random.choice(plant_types)
                        npc["action_timer"] = 30  # Giảm thời gian hành động
                        npc["target"] = None
                    elif npc["task"] == "harvest" and game_map[tile_y][tile_x] in mature_plants:
                        game_map[tile_y][tile_x] = "D"
                        npc["action_timer"] = 30
                        npc["target"] = None
                    elif npc["task"] == "fish" and tile_y == river_y_start - 1 and game_map[tile_y][tile_x] != "W":
                        npc["action_timer"] = 120
                        npc["target"] = None
        else:
            npc["target"] = None
    else:
        if random.random() < 0.02:
            direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
            if direction.length() > 0:
                direction = direction.normalize()
                new_pos = npc["pos"] + direction * 4
                if not check_tile_collision(new_pos, npc["size"]):
                    npc["pos"] = new_pos
                    if abs(direction.x) > abs(direction.y):
                        npc["direction"] = "right" if direction.x > 0 else "left"
                    else:
                        npc["direction"] = "down" if direction.y > 0 else "up"
                    npc["animation_timer"] += 1
                    if npc["animation_timer"] >= ANIMATION_SPEED:
                        npc["frame"] = (npc["frame"] + 1) % 2
                        npc["animation_timer"] = 0

# Main game loop
running = True

while running:
    screen.fill((0, 0, 0))

    # --- Input ---
    keys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)
    if keys[pygame.K_w]: 
        direction.y -= 1
        player_direction = "up"
    if keys[pygame.K_s]: 
        direction.y += 1
        player_direction = "down"
    if keys[pygame.K_a]: 
        direction.x -= 1
        player_direction = "left"
    if keys[pygame.K_d]: 
        direction.x += 1
        player_direction = "right"
    if direction.length() > 0:
        direction = direction.normalize()
        animation_timer += 1
        if animation_timer >= ANIMATION_SPEED:
            player_frame = (player_frame + 1) % 2
            animation_timer = 0
    else:
        player_frame = 0

    # --- Update ---
    new_pos = player_pos + direction * player_speed
    temp_pos = player_pos + pygame.Vector2(direction.x * player_speed, 0)
    if not check_tile_collision(temp_pos, player_size):
        player_pos.x = temp_pos.x
    temp_pos = player_pos + pygame.Vector2(0, direction.y * player_speed)
    if not check_tile_collision(temp_pos, player_size):
        player_pos.y = temp_pos.y

    # Ràng buộc trong map
    player_pos.x = max(0, min(player_pos.x, MAP_WIDTH * TILE_SIZE - player_size))
    player_pos.y = max(0, min(player_pos.y, MAP_HEIGHT * TILE_SIZE - player_size))

    # Cập nhật thú cưng của người chơi
    update_pet(player_pet, player_pos, player_direction)

    # Cập nhật NPC và thú cưng của họ
    for npc in npcs:
        update_npc(npc, game_map, farm_x, farm_y, river_y_start)
        update_pet(npc["pet"], npc["pos"], npc["direction"])

    # Cập nhật gia súc
    for animal in animals:
        update_animal(animal, barn_x, barn_y)

    # Cập nhật cây trồng
    plant_growth_timer += 1
    if plant_growth_timer >= PLANT_GROWTH_INTERVAL:
        plant_growth_timer = 0
        for y in range(farm_y, farm_y + 10):
            for x in range(farm_x, farm_x + 10):
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    if game_map[y][x] == "P1" and random.random() < 0.2:
                        game_map[y][x] = "P4"
                    elif game_map[y][x] == "P2" and random.random() < 0.2:
                        game_map[y][x] = "P5"
                    elif game_map[y][x] == "P3" and random.random() < 0.2:
                        game_map[y][x] = "P6"

    # Tính camera offset
    camera_offset_x = int(player_pos.x - SCREEN_WIDTH // 2 + player_size // 2)
    camera_offset_y = int(player_pos.y - SCREEN_HEIGHT // 2 + player_size // 2)

    # Kiểm tra gợi ý tương tác
    nearby_plant = check_nearby_plant(player_pos, game_map)
    prompt_text = None
    if check_nearby_npc(player_pos, npcs):
        prompt_text = "Bạn có muốn nói chuyện không?"
    elif nearby_plant:
        prompt_text = "Nhấn E để thu hoạch"

    # Xử lý tương tác
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if check_nearby_npc(player_pos, npcs):
                    dialogue_text = "Hey hey!"
                    dialogue_timer = DIALOGUE_DURATION
                elif nearby_plant:
                    x, y = nearby_plant
                    game_map[y][x] = "D"

    # Cập nhật timer đối thoại
    if dialogue_timer > 0:
        dialogue_timer -= 1
        if dialogue_timer == 0:
            dialogue_text = None

    # --- Draw ---
    draw_map(camera_offset_x, camera_offset_y)

    # Vẽ gia súc
    for animal in animals:
        animal_screen_x = animal["pos"].x - camera_offset_x
        animal_screen_y = animal["pos"].y - camera_offset_y
        if (0 <= animal_screen_x <= SCREEN_WIDTH and 0 <= animal_screen_y <= SCREEN_HEIGHT):
            draw_animal(screen, animal_screen_x, animal_screen_y, animal["size"], 
                        animal["type"], animal["direction"], animal["frame"])

    # Vẽ NPC và thú cưng của họ
    for npc in npcs:
        npc_screen_x = npc["pos"].x - camera_offset_x
        npc_screen_y = npc["pos"].y - camera_offset_y
        if (0 <= npc_screen_x <= SCREEN_WIDTH and 0 <= npc_screen_y <= SCREEN_HEIGHT):
            draw_character(screen, npc_screen_x, npc_screen_y, npc["size"], 
                          is_player=False, direction=npc["direction"], frame=npc["frame"])
            if npc["action_timer"] > 0 and npc["task"]:
                draw_task_effect(screen, npc_screen_x, npc_screen_y, npc["task"])
        pet_screen_x = npc["pet"]["pos"].x - camera_offset_x
        pet_screen_y = npc["pet"]["pos"].y - camera_offset_x
        if (0 <= pet_screen_x <= SCREEN_WIDTH and 0 <= pet_screen_y <= SCREEN_HEIGHT):
            draw_animal(screen, pet_screen_x, pet_screen_y, npc["pet"]["size"], 
                        "wolf", npc["pet"]["direction"], npc["pet"]["frame"])

    # Vẽ người chơi và thú cưng
    draw_character(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, player_size, 
                   is_player=True, direction=player_direction, frame=player_frame)
    pet_screen_x = player_pet["pos"].x - camera_offset_x
    pet_screen_y = player_pet["pos"].y - camera_offset_y
    if (0 <= pet_screen_x <= SCREEN_WIDTH and 0 <= pet_screen_y <= SCREEN_HEIGHT):
        draw_animal(screen, pet_screen_x, pet_screen_y, player_pet["size"], 
                    "wolf", player_pet["direction"], player_pet["frame"])

    # Vẽ HUD
    draw_hud(player_pos, npcs, game_map)

    # Vẽ gợi ý
    if prompt_text:
        text_surface = font.render(prompt_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        pygame.draw.rect(screen, (20, 20, 20, 200), text_rect.inflate(20, 12))
        pygame.draw.rect(screen, (100, 100, 100), text_rect.inflate(20, 12), 2)
        screen.blit(text_surface, text_rect)

    # Vẽ đối thoại
    if dialogue_text:
        text_surface = font.render(dialogue_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        pygame.draw.rect(screen, (20, 20, 20, 200), text_rect.inflate(20, 12))
        pygame.draw.rect(screen, (100, 100, 100), text_rect.inflate(20, 12), 2)
        screen.blit(text_surface, text_rect)

    # --- Refresh ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()