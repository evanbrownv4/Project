import pygame
import pygame_gui
import math
import random

from highscore_table import HighscoreTable
from server_connector import DatabaseConnector

# A bunch of constants
# Screen resolution, x width by y height in pixels
resolution = (1000, 700)
# Bounds of screen actually used for the game
play_space = (resolution[0], resolution[1] - 100)
# FPS
fps = 1 / 60
# Dictionary of colours
colours = {"White": (255, 255, 255), "Black": (0, 0, 0)}

class Paddle:
    paddle_y_padding = 20
    velocity = 10

    paddle_size = [150, 15]
    # Initial paddle position
    initial_position = [
        play_space[0] / 2 - paddle_size[0] / 2,  # X-Coord
        play_space[1] - paddle_size[1] - paddle_y_padding  # Y-Coord
    ]

    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.position = Paddle.initial_position[:]

    def move(self, key_inputs):
        if key_inputs[pygame.K_LEFT]:
            self.move_left()
        if key_inputs[pygame.K_RIGHT]:
            self.move_right()

    # Logic for moving paddle right
    def move_right(self):
        # Calculate position of the paddle in the next frame:
        predicted_pos = self.position[0] + self.velocity
        # If the paddle is predicted to clip outside the bounds of the screen on the right side:
        if predicted_pos > (play_space[0] - self.paddle_size[0]):
            # Don't let it, set its position to be just on the edge
            self.position[0] = play_space[0] - self.paddle_size[0]
        # Else
        else:
            # Let it move normally
            self.position[0] = predicted_pos

    # Logic for moving paddle left
    def move_left(self):
        # Calculate position of the paddle in the next frame
        predicted_pos = self.position[0] - self.velocity
        # If the paddle is predicted to clip outside the bounds of the screen on the left side:
        if predicted_pos < 0:
            # Don't let it, set its position to be just on the edge
            self.position[0] = 0
        # Else
        else:
            # Let it move normally
            self.position[0] = predicted_pos

    def draw(self):
        pygame.draw.rect(self.parent_screen, colours["White"], self.position + self.paddle_size)


class Projectile:
    init_speed = 5

    initial_pos = [play_space[0] / 2, play_space[1] * 0.2]

    radius = 8

    def __init__(self, parent_screen, paddle):
        self.parent_screen = parent_screen
        self.paddle = paddle

        self.angle = random.uniform(-math.pi / 4, math.pi / 4)
        self.speed = int(Projectile.init_speed)
        self.position = Projectile.initial_pos[:]

        self.x_velocity = None
        self.y_velocity = None
        self.set_component_velocities()

    def draw(self):
        pygame.draw.circle(self.parent_screen, colours["White"], (self.position[0], self.position[1]), self.radius)

    def set_component_velocities(self):
        self.x_velocity = self.speed * math.sin(self.angle)
        self.y_velocity = self.speed * math.cos(self.angle)

    def move(self):
        next_position = [self.position[0] + self.x_velocity, self.position[1] + self.y_velocity]
        self.handle_wall_collision(next_position)
        self.handle_paddle_collision(next_position)

    def handle_wall_collision(self, new_position):
        # If there's a collision on the top
        if new_position[1] < self.radius:
            # Reverse the direction of the y velocity
            self.y_velocity = -self.y_velocity
            # Set the y position to the top of the screen
            self.position[1] = self.radius

        # Else if there's no collision along the y-axis:
        else:
            # Increment the position by the y_velocity
            self.position[1] = self.position[1] + self.y_velocity

        # If there's a left collision
        if new_position[0] < self.radius:
            # Reverse the direction of the y velocity
            self.x_velocity = -1 * self.x_velocity
            # Set the x position to the left of the screen
            self.position[0] = self.radius

        # If there's a right collision
        if new_position[0] > play_space[0] - self.radius:
            # Reverse the direction of the y velocity
            self.x_velocity = -1 * self.x_velocity
            # Set the x position to the right of the screen
            self.position[0] = play_space[0] - self.radius

        # Else if there's no collision along the y-axis:
        else:
            # Increment the position by the x velocity
            self.position[0] += self.x_velocity

    def handle_paddle_collision(self, new_position):
        # Paddle collisions only possible while moving down
        if self.y_velocity > 0:
            # Get paddle position and size
            paddle_pos = self.paddle.position
            paddle_size = self.paddle.paddle_size

            IN_X_BOUNDS = paddle_pos[0] - self.radius < self.position[0] < paddle_pos[0] + paddle_size[0] + self.radius
            IN_Y_BOUNDS = paddle_pos[1] < new_position[1] + self.radius < paddle_pos[1] + self.y_velocity

            if IN_X_BOUNDS and IN_Y_BOUNDS:
                # Set projectiles y position to on the paddle
                self.position[1] = paddle_pos[1] - self.radius

                # Calculate offset from projectile x to center of the paddle
                delta_x = self.position[0] - (paddle_pos[0] + (paddle_size[0] / 2))
                # Change the angle of the projectile based on the offset
                # Add a small randomness to the new angle, approximately between ±5 degrees
                self.angle = (2 * delta_x) / paddle_size[0]

                # Increment speed
                self.speed += 0.5

                # Update component velocities
                self.set_component_velocities()
                # Reverse the direction of the y velocity
                self.y_velocity = -1 * self.y_velocity

                # Increment score by 1
                Game.score += 1


class Game:
    # Keeps track of score
    score = 0

    running = True

    def __init__(self, user_id, window_surface, ui_manager):
        # Surface to draw on
        self.window_surface = window_surface
        # UI manager
        self.ui_manager = ui_manager
        # User ID for updating score
        self.user_id = user_id
        # Username for writing labels and stuff
        self.username = DatabaseConnector.get_username(user_id)
        # Creates a clock
        self.clock = pygame.time.Clock()
        # Game over state initially false
        self.dead = False
        # Create a paddle
        self.paddle = Paddle(window_surface)
        # Create a projectile
        self.projectile = Projectile(window_surface, self.paddle)

    # Get inputs
    @staticmethod
    def get_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        return pygame.key.get_pressed()

    def move(self, inputs):
        self.paddle.move(inputs)
        self.projectile.move()
        self.check_game_over()

    # Draw next frame
    def draw_new_frame(self):
        # Refresh the screen
        self.window_surface.fill(colours["Black"])
        # Draw the new paddle
        self.paddle.draw()
        # Draw the projectile
        self.projectile.draw()
        # Draw UI
        self.draw_UI()

    # Draw basic UI
    def draw_UI(self):
        pygame.draw.lines(self.window_surface, colours["White"], True,
                          [(0, 1), (0, play_space[1]), (play_space[0] - 1, play_space[1]), (play_space[0] - 1, 1)])
        font_obj = pygame.font.SysFont("arial", 30)

        score_label = font_obj.render(f"Score: {self.score}", True, colours["White"])
        self.window_surface.blit(score_label, (10, play_space[1] + 20))

    def kill_UI(self, container):
        container.kill()
        # Update manager
        self.ui_manager.update(1)
        # Fill screen with black
        self.window_surface.fill("black")
        # Refresh screen
        pygame.display.update()

    # Check game over
    def check_game_over(self):
        next_position = self.projectile.position[1] + self.projectile.y_velocity
        if next_position + self.projectile.radius >= play_space[1]:
            self.projectile.position[1] = play_space[1] - self.projectile.radius
            self.dead = True

    def update_score(self):
        current_score = DatabaseConnector.get_score(self.user_id)
        if self.score > current_score:
            DatabaseConnector.update_score(self.user_id, self.score)

    def start(self):
        # Draw initial frame
        self.draw_new_frame()
        pygame.display.flip()

        start_prompt_container = pygame_gui.core.ui_container.UIContainer(
            relative_rect=pygame.Rect((250, 350), (500, 100)),
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (500, 50)),
            text="Move using the left and right arrow keys.",
            container=start_prompt_container
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 50), (300, 50)),
            text="Start moving to start the game.",
            container=start_prompt_container
        )

        # Wait for a valid input
        started = False
        while not started:

            # Draw UI labels
            self.ui_manager.draw_ui(self.window_surface)
            # Update manager
            self.ui_manager.update(1)
            # Refresh screen
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
                started = True
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()
                started = True

        self.kill_UI(start_prompt_container)

    def main_game_loop(self):
        # While the player has not entered anything inputs, initially pause the game
        self.start()

        # While alive:
        while not self.dead:
            self.clock.tick(60)
            # Return inputs and do stuff with them
            key_inputs = self.get_input()
            # Calculate next frame
            self.move(key_inputs)
            # Draw next frame
            self.draw_new_frame()
            # Refresh screen to display next frame
            pygame.display.flip()

    def game_over_loop(self):
        # Update score
        self.update_score()
        # Draw the game over screen
        self.window_surface.fill(colours["Black"])

        game_over_container = pygame_gui.core.ui_container.UIContainer(
            relative_rect=pygame.Rect((0, 0), resolution),
            manager=self.ui_manager
        )

        game_over_rect = pygame.Rect((0, 10), (300, 30))
        game_over_rect.centerx = resolution[0]/2

        pygame_gui.elements.UILabel(
            relative_rect=game_over_rect,
            text="Game over!",
            container=game_over_container
        )

        score_rect = pygame.Rect((0, 50), (500, 30))
        score_rect.centerx = resolution[0] / 2

        pygame_gui.elements.UILabel(
            relative_rect=score_rect,
            text=f"You lost playing as {self.username} with a score of {self.score}.",
            container=game_over_container
        )

        highscore_rect = pygame.Rect((0, 100), (500, 330))
        highscore_rect.centerx = resolution[0] / 2

        # High score table
        HighscoreTable.create_highscore_table(
            relative_rect=highscore_rect,
            manager=self.ui_manager,
            container=game_over_container
        )

        search_rect = pygame.Rect((0, 450), (300, 150))
        search_rect.centerx = resolution[0] / 2

        # Search user field
        entry_field, enter_button, result_label = HighscoreTable.create_search_field(
            relative_rect=search_rect,
            manager=self.ui_manager,
            container=game_over_container
        )

        play_again_rect = pygame.Rect((0, 630), (150, 50))
        play_again_rect.centerx = (resolution[0]/3) * 1

        # Draw play again button
        play_again = pygame_gui.elements.UIButton(
            relative_rect=play_again_rect,
            text="Play again",
            container=game_over_container
        )

        log_out_rect = pygame.Rect((0, 630), (150, 50))
        log_out_rect.centerx = resolution[0] / 2

        # Create log out button
        log_out_button = pygame_gui.elements.UIButton(
            relative_rect=log_out_rect,
            text="Log Out",
            container=game_over_container
        )

        quit_rect = pygame.Rect((0, 630), (150, 50))
        quit_rect.centerx = (resolution[0] / 3) * 2

        # Create quit button
        quit_button = pygame_gui.elements.UIButton(
            relative_rect=quit_rect,
            text="Quit",
            container=game_over_container
        )

        button_clicked = False
        while not button_clicked:

            # Draw UI buttons
            self.ui_manager.draw_ui(self.window_surface)
            # Update manager
            self.ui_manager.update(1)
            # Refresh screen
            pygame.display.update()

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                elif ev.type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == play_again:
                        self.game_restart()
                        button_clicked = True

                    elif ev.ui_element == log_out_button:
                        self.running = False
                        button_clicked = True

                    elif ev.ui_element == quit_button:
                        quit()

                    elif ev.ui_element == enter_button:
                        result_label.set_text(HighscoreTable.search_users_score(entry_field.get_text()))

                self.ui_manager.process_events(ev)

        self.kill_UI(game_over_container)

    def game_restart(self):
        # Reset the score
        Game.score = 0
        # Set our paddle object to a new instance of the Paddle class
        self.paddle = Paddle(self.window_surface)
        # Set our projectile object to a new instance of the Projectile class
        self.projectile = Projectile(self.window_surface, self.paddle)
        # Set our game over variable to false, allowing the rest of the game to run normally
        self.dead = False

    def run_game(self):
        # Do actual game stuff
        self.main_game_loop()
        # Do game over stuff
        self.game_over_loop()
