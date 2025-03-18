# Kích thước màn hình
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Năng lượng
DEFAULT_ENERGY = 100  # Năng lượng mặc định của người chơi
MAX_ENERGY = 100      # Năng lượng tối đa ban đầu
ENERGY_COSTS = {
    "plant_seed": 10,  # Tốn năng lượng khi gieo hạt
    "water_plant": 5,  # Tốn năng lượng khi tưới cây
    "harvest": 0,      # Không tốn năng lượng khi thu hoạch
    "dig": 0,          # Không tốn năng lượng khi đào hạt
    "fish": 10         # Tốn năng lượng khi câu cá
}
ENERGY_HERB_BOOST = 20  # Tăng năng lượng khi dùng thảo mộc tăng năng lượng

# Thời gian trồng cây (số ngày)
PLANT_GROWTH_TIME = {
    "carrot": 2,       # Hạt giống ngắn ngày
    "cabbage": 2,
    "tomato": 3,       # Hạt giống dài ngày
    "potato": 3,
    "energy_herb": 3,  # Hạt giống đặc biệt
    "rare_herb": 3
}

# Giá mua/bán nông sản (đồng)
FARM_PRICES = {
    "carrot": {"buy": 3, "sell": 2},
    "cabbage": {"buy": 4, "sell": 3},
    "tomato": {"buy": 7, "sell": 5},
    "potato": {"buy": 9, "sell": 6},
    "energy_herb": {"buy": None, "sell": None},  # Không mua/bán, dùng trực tiếp
    "rare_herb": {"buy": 15, "sell": 10}         # Có thể mua và bán
}

# Giá mua/bán ngư sản (đồng)
FISH_PRICES = {
    "tilapia": {"buy": None, "sell": 4},    # Cá rô phi
    "carp": {"buy": None, "sell": 6},       # Cá chép
    "catfish": {"buy": None, "sell": 5},    # Cá trê
    "eel": {"buy": None, "sell": 7},        # Cá chình
    "ghost_fish": {"buy": None, "sell": 8}, # Cá ma
    "frog": {"buy": None, "sell": 3}        # Ếch
}

# Giá nâng cấp cần câu (đồng)
ROD_UPGRADE_COSTS = {
    "silver": 20,  # Gỗ -> Bạc
    "gold": 25,    # Bạc -> Vàng
    "diamond": 32  # Vàng -> Kim Cương
}

# Giá mở rộng vườn (đồng)
GARDEN_UPGRADE_COSTS = {
    6: 18,  # 4 ô -> 6 ô
    8: 25,  # 6 ô -> 8 ô
    10: 32  # 8 ô -> 10 ô
}

# Cấu hình minigame câu cá
FISHING_BAR_WIDTH = 50
FISHING_BAR_HEIGHT = 412
FISHING_FISH_SIZE = 40
FISHING_GREEN_ZONE_SIZE = {
    "wood": 100,    # Cần gỗ
    "silver": 120,  # Cần bạc
    "gold": 140,    # Cần vàng
    "diamond": 160  # Cần kim cương
}
FISHING_MAX_OUTSIDE_TIME = 3  # Thời gian tối đa cá ngoài vùng xanh (giây)
FISHING_SUCCESS_TIME = 5      # Thời gian giữ cá trong vùng xanh để thắng (giây)

# Danh sách cá theo thời gian trong ngày
FISH_DAY = ["tilapia", "carp", "frog"]              # Sáng
FISH_NIGHT = ["catfish", "eel", "ghost_fish", "frog"]  # Tối