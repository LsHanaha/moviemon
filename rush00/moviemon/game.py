import pickle
from django.conf import settings as django_settings
import os


class Game:
    def __init__(self, current_point: tuple[int, int], moviemons: dict[str, dict[str, any]], movieballs_count):
        self._field_size = 20
        self._current_point = current_point
        self._movieballs_count = movieballs_count
        self._moviemons = moviemons
        self._captured_movies = []
        self._game_map = None

    def dump(self, game_name="default"):
        with open(os.path.join(django_settings.BASE_DIR, 'moviemon', game_name), 'w') as f:
            pickle.dump(self, f)

    def _init_game_map(self):
        pass


class GameManager:

    def __init__(self):
        self.game = None

    def load(self, filename: str):
        filepath = os.path.join(django_settings.BASE_DIR, 'moviemon', filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filename} does not exist. "
                                    f"Send your Gameboy to the local authorized center")
        with open(filepath, 'r') as f:
            game_instance = pickle.load(f)
        self.game = game_instance
        return game_instance

    def dump(self, filename="default"):
        if not self.game:
            raise Exception("Game not exist, can't dump nothing")
        self.game.dump(filename)

    def get_random_movie(self):
        pass

    def load_default_settings(self):
        pass

    def get_strength(self):
        pass

    def get_movie(self):
        pass




