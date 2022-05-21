import pickle
import os
import random
from django.conf import settings as django_settings


class Game:
    def __init__(self,
                 current_point: tuple[int, int],
                 movieballs_count: int,
                 moviemons: dict[str, dict[str, any]]):
        self._field_size = 15
        self._current_point = current_point
        self._movieballs_count = movieballs_count
        self._moviemons = moviemons
        self._enemies_count = 15
        self._balls_treasures_count = 20
        self._captured_movies = []
        self._game_map = None

    def dump(self, game_name="current"):
        with open(os.path.join(django_settings.BASE_DIR, 'moviemon', game_name), 'w') as f:
            pickle.dump(self, f)

    def _init_game_map(self):
        pass

    def get_random_movie(self):
        pass

    def load_default_settings(self):
        pass

    def get_strength(self):
        pass

    def get_movie(self):
        pass


class GameManager:

    @classmethod
    def load(cls, filename: str):
        filepath = os.path.join(django_settings.BASE_DIR, 'moviemon', filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filename} does not exist. "
                                    f"Send your Gameboy to the local authorized center")
        with open(filepath, 'r') as f:
            game_instance = pickle.load(f)
        return game_instance

    @classmethod
    def dump(cls, game: Game, filename="current") -> None:
        filepath = os.path.join(django_settings.BASE_DIR, 'moviemon', filename)
        with open(filepath, 'w') as f:
            pickle.dump(game, f)


def start_new_game():
    game = Game((random.randint(0, 15), random.randint(0, 15)), 15, {})




