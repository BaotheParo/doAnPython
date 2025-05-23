import pygame
import os
from src.core.game_state import GameState
from src.core.ui import SettingsUI
from src.scenes.menu import MainMenu
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Định nghĩa đường dẫn tới thư mục soundeffect
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    MUSIC_PATH = os.path.join(BASE_DIR, "doAnPython", "assets", "soundeffect")

    # Khởi tạo và phát background music
    pygame.mixer.init()
    music_file = os.path.join(MUSIC_PATH, "background_music.mp3")
    if os.path.exists(music_file):  # Kiểm tra file có tồn tại không
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5)  # Đặt âm lượng (0.0 đến 1.0)
            pygame.mixer.music.play(-1)  # Phát music, -1 để lặp vô hạn
        except pygame.error as e:
            print(f"Không thể tải background music: {e}")
    else:
        print(f"File music không tồn tại: {music_file}")

    # Khởi tạo game_state và settings_ui trước khi tạo MainMenu
    game_state = GameState()
    settings_ui = SettingsUI(screen, game_state)
    current_scene = MainMenu(screen, game_state, settings_ui)  # Truyền cả screen, game_state và ui

    # Vòng lặp chính để quản lý các scene
    while current_scene:
        next_scene = current_scene.run()
        current_scene = next_scene

    pygame.mixer.music.stop()  # Dừng music khi thoát trò chơi
    pygame.quit()


if __name__ == "__main__":
    main()