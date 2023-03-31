import pygame
import pygame_gui
from pygame_login_window import LoginWindow

from pong_demo import Game

pygame.init()

resolution = (1000, 700)
pygame.display.set_caption("Lonely Pong")
window_surface = pygame.display.set_mode(resolution)
ui_manager = pygame_gui.UIManager(resolution, 'data/themes/pygame_gui_themes.json')

if __name__ == "__main__":
    login_window = LoginWindow(ui_manager, window_surface, resolution)
    while True:
        user_id = login_window.run()
        game = Game(user_id, window_surface, ui_manager)
        while game.running:
            game.run_game()
