import pygame_gui
import pygame
from global_algorithms import bubble_sort, binary_search
from AHProject.server_connector import DatabaseConnector

class LoginWindow:

    def __init__(self, ui_manager, window_surface, resolution):
        self.ui_manager = ui_manager
        self.window_surface = window_surface
        self.resolution = resolution

    def get_login_screen(self):

        container_rect = pygame.Rect((0, 0), (200, 250))
        container_rect.centerx, container_rect.centery = round(self.resolution[0] / 2), round(self.resolution[1] / 2)

        login_container = pygame_gui.core.UIContainer(
            relative_rect=container_rect,
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 10), (100, 30)),
            text="Login!",
            manager=self.ui_manager,
            container=login_container
        )

        username_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 50), (200, 50)),
            placeholder_text="Username",
            manager=self.ui_manager,
            container=login_container
        )

        password_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 100), (200, 50)),
            placeholder_text="Password",
            manager=self.ui_manager,
            container=login_container
        )

        submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 150), (100, 50)),
            text="Submit",
            manager=self.ui_manager,
            container=login_container
        )

        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 150), (100, 50)),
            text="Back",
            manager=self.ui_manager,
            container=login_container
        )

        response_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 210), (160, 30)),
            text="",
            manager=self.ui_manager,
            container=login_container
        )

        return login_container, username_field, password_field, submit_button, back_button, response_label

    def login(self):
        clock = pygame.time.Clock()

        login_container, username_field, password_field, submit_button, back_button, response_label = self.get_login_screen()

        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == submit_button:

                        ENTERED_USERNAME, ENTERED_PASSWORD = username_field.get_text(), password_field.get_text()

                        all_users = DatabaseConnector.select_all()
                        bubble_sort(all_users, sort_by="username", order="asc")
                        user_index = binary_search(all_users, ENTERED_USERNAME)
                        if user_index is None:
                            response_label.set_text("Invalid username")
                            continue
                        user = all_users[user_index]

                        if user.password != ENTERED_PASSWORD:
                            response_label.set_text("Invalid password")
                            continue

                        LOGGED_IN = True
                        running = False

                    elif event.ui_element == back_button:
                        running = False
                        LOGGED_IN = False

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

        self.kill_container(login_container)

        if LOGGED_IN:
            return user.user_id
        else:
            return None

    def get_create_screen(self):

        container_rect = pygame.Rect((0, 0), (200, 250))
        container_rect.centerx, container_rect.centery = round(self.resolution[0] / 2), round(self.resolution[1] / 2)

        create_container = pygame_gui.core.UIContainer(
            relative_rect=container_rect,
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 10), (100, 30)),
            text="Create User",
            manager=self.ui_manager,
            container=create_container
        )

        username_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 50), (200, 50)),
            placeholder_text="Username",
            manager=self.ui_manager,
            container=create_container
        )

        password_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 100), (200, 50)),
            placeholder_text="Password",
            manager=self.ui_manager,
            container=create_container
        )

        submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 150), (100, 50)),
            text="Submit",
            manager=self.ui_manager,
            container=create_container
        )

        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 150), (100, 50)),
            text="Back",
            manager=self.ui_manager,
            container=create_container
        )

        response_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 210), (160, 30)),
            text="",
            manager=self.ui_manager,
            container=create_container
        )

        return create_container, username_field, password_field, submit_button, back_button, response_label

    def create_account(self):
        clock = pygame.time.Clock()

        create_container, username_field, password_field, submit_button, back_button, response_label = self.get_create_screen()

        all_users = DatabaseConnector.select_all()

        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == submit_button:

                        ENTERED_USERNAME, ENTERED_PASSWORD = username_field.get_text(), password_field.get_text()

                        EMPTY_FIELD = ENTERED_USERNAME == "" or ENTERED_PASSWORD == ""
                        if EMPTY_FIELD:
                            response_label.set_text(
                                "Please enter a value"
                            )
                            response_label.rebuild()
                            continue

                        bubble_sort(unsorted_array=all_users, sort_by="username")
                        IS_UNIQUE_USERNAME = binary_search(all_users, ENTERED_USERNAME) is None

                        if IS_UNIQUE_USERNAME:
                            DatabaseConnector.create_user(ENTERED_USERNAME, ENTERED_PASSWORD)
                            running = False
                        else:
                            response_label.set_text(
                                "A user with this username already exists, please enter a new username."
                            )
                            response_label.rebuild()

                    elif event.ui_element == back_button:
                        running = False

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

        self.kill_container(create_container)

    def get_update_screen(self):

        container_rect = pygame.Rect((0, 0), (200, 300))
        container_rect.centerx, container_rect.centery = round(self.resolution[0]/2), round(self.resolution[1]/2)

        update_container = pygame_gui.core.UIContainer(
            relative_rect=container_rect,
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 10), (100, 30)),
            text="Update User",
            manager=self.ui_manager,
            container=update_container
        )

        username_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 50), (200, 50)),
            placeholder_text="Username",
            manager=self.ui_manager,
            container=update_container
        )

        old_password_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 100), (200, 50)),
            placeholder_text="Old Password",
            manager=self.ui_manager,
            container=update_container
        )

        new_password_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 150), (200, 50)),
            placeholder_text="New Password",
            manager=self.ui_manager,
            container=update_container
        )

        submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 200), (100, 50)),
            text="Submit",
            manager=self.ui_manager,
            container=update_container
        )

        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 200), (100, 50)),
            text="Back",
            manager=self.ui_manager,
            container=update_container
        )

        response_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 260), (160, 30)),
            text="",
            manager=self.ui_manager,
            container=update_container
        )

        return update_container, username_field, old_password_field, new_password_field, submit_button, back_button, response_label

    def update_account(self):
        clock = pygame.time.Clock()

        update_container, username_field, old_password_field, new_password_field, submit_button, back_button, response_label = self.get_update_screen()

        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == submit_button:

                        ENTERED_USERNAME = username_field.get_text()
                        ENTERED_OLD_PASS = old_password_field.get_text()
                        ENTERED_NEW_PASS = new_password_field.get_text()

                        if ENTERED_USERNAME == "" or ENTERED_OLD_PASS == "" or ENTERED_NEW_PASS == "":
                            response_label.set_text("Fields cant be empty")
                            response_label.rebuild()
                            continue

                        all_users = DatabaseConnector.select_all()
                        bubble_sort(all_users)

                        user_index = binary_search(all_users, ENTERED_USERNAME)

                        if user_index is None:
                            response_label.set_text("Invalid username")
                            continue
                        user = all_users[user_index]

                        if user.password != ENTERED_OLD_PASS:
                            response_label.set_text("Invalid old password")
                            continue

                        if ENTERED_NEW_PASS == ENTERED_OLD_PASS:
                            response_label.set_text("New password cant be the same as the old password")
                            continue

                        DatabaseConnector.update_password(ENTERED_USERNAME, ENTERED_NEW_PASS)
                        running = False

                    elif event.ui_element == back_button:
                        running = False

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

        self.kill_container(update_container)

    def get_start_screen(self):
        start_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((0, 0), self.resolution),
            manager=self.ui_manager
        )

        name_rect = pygame.Rect((0, 50), (200, 50))
        name_rect.centerx = round(self.resolution[0]/2)

        pygame_gui.elements.UILabel(
            relative_rect=name_rect,
            text="Lonely Pong!",
            manager=self.ui_manager,
            container=start_container
        )

        login_rect = pygame.Rect((0, 200), (250, 50))
        login_rect.centerx = round(self.resolution[0] / 3) - 100

        login_button = pygame_gui.elements.UIButton(
            relative_rect=login_rect,
            text="Log In!",
            manager=self.ui_manager,
            container=start_container
        )

        create_rect = pygame.Rect((0, 200), (250, 50))
        create_rect.centerx = round(self.resolution[0] / 2)

        create_button = pygame_gui.elements.UIButton(
            relative_rect=create_rect,
            text="Create Account",
            manager=self.ui_manager,
            container=start_container
        )

        update_rect = pygame.Rect((0, 200), (250, 50))
        update_rect.centerx = round(self.resolution[0] / 3)*2 + 100

        update_button = pygame_gui.elements.UIButton(
            relative_rect=update_rect,
            text="Update Username/Password",
            manager=self.ui_manager,
            container=start_container
        )

        quit_rect = pygame.Rect((0, 400), (200, 50))
        quit_rect.centerx = round(self.resolution[0]/2)

        quit_button = pygame_gui.elements.UIButton(
            relative_rect=quit_rect,
            text="Quit :(",
            manager=self.ui_manager,
            container=start_container
        )

        return start_container, login_button, create_button, update_button, quit_button

    def run(self):
        clock = pygame.time.Clock()

        start_screen, login_button, create_button, update_button, quit_button = self.get_start_screen()

        running = True
        while running:

            time_delta = clock.tick(60) / 1000.0

            self.ui_manager.update(time_delta)
            self.window_surface.blit(self.window_surface, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)
            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == login_button:

                        self.kill_container(start_screen)
                        current_user_id = self.login()
                        SUCCESSFUL_LOGIN = True if current_user_id is not None else False

                        if SUCCESSFUL_LOGIN:
                            running = False

                        else:
                            start_screen, login_button, create_button, update_button, quit_button = self.get_start_screen()

                    elif event.ui_element == create_button:
                        self.kill_container(start_screen)
                        self.create_account()
                        start_screen, login_button, create_button, update_button, quit_button = self.get_start_screen()

                    elif event.ui_element == update_button:
                        self.kill_container(start_screen)
                        self.update_account()
                        start_screen, login_button, create_button, update_button, quit_button = self.get_start_screen()

                    elif event.ui_element == quit_button:
                        quit()

                self.ui_manager.process_events(event)

        return current_user_id

    def kill_container(self, container):
        container.kill()
        self.ui_manager.update(1)
        self.window_surface.fill("black")
        pygame.display.update()
