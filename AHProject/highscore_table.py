import pygame
import pygame_gui
from global_algorithms import bubble_sort, binary_search
from server_connector import DatabaseConnector

class HighscoreTable:

    @staticmethod
    def get_top_ten():
        all_users = DatabaseConnector.select_all()
        # Sort users by score
        bubble_sort(all_users, sort_by="score",)
        top_ten = all_users[:10:-1]
        return top_ten

    @staticmethod
    def create_highscore_table(relative_rect, manager, container):
        top_ten = HighscoreTable.get_top_ten()
        highscore_table = pygame_gui.core.ui_container.UIContainer(
            relative_rect=relative_rect,
            manager=manager,
            container=container)

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (500, 30)),
            text=f"Top 10 Users:",
            container=highscore_table
        )

        for i in range(len(top_ten)):
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((0, (i + 1) * 30), (500, 30)),
                text=f"{i + 1}: {top_ten[i].username} with a score of {top_ten[i].score}",
                container=highscore_table
            )

        return highscore_table

    @staticmethod
    def search_users_score(search_username):
        all_users = DatabaseConnector.select_all()
        bubble_sort(all_users, sort_by="username")

        search_result = binary_search(all_users, search_username)

        if search_result is None:
            return "No such user exists."
        else:
            requested_user = all_users[search_result]
            return f"{requested_user.username}'s score is {requested_user.score}"

    @staticmethod
    def create_search_field(relative_rect, manager, container):
        search_user = pygame_gui.core.ui_container.UIContainer(
            relative_rect=relative_rect,
            manager=manager,
            container=container)

        entry_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 0), (300, 50)),
            manager=manager,
            container=search_user,
            placeholder_text="Enter Username"
        )

        enter_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 50), (300, 50)),
            manager=manager,
            container=search_user,
            text="Search!"
        )

        result_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 100), (300, 50)),
            manager=manager,
            container=search_user,
            text=""
        )

        return entry_field, enter_button, result_label
