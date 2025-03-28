import pygame
from src.core.game_state import GameState
from src.core.ui import SettingsUI
from src.scenes.farm import FarmScene
from src.scenes.fishing import FishingScene
from src.scenes.bedroom import Bedroom
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    game_state = GameState()
    settings_ui = SettingsUI(screen, game_state)
    current_scene = Bedroom(game_state, screen, settings_ui)
    
    while True:
        current_scene.run()
        break
    
    pygame.quit()

if __name__ == "__main__":
    main()

