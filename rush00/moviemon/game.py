import pickle
import os
import random
import typing

from django.conf import settings as django_settings


class Game:

    PLAYER = 1
    MONSTER = 2
    POKEBALL = 3

    _max_pokeballs_count = 25

    def __init__(self,
                 current_point: tuple[int, int],
                 movieballs_count: int,
                 moviemons: dict[str, dict[str, any]]):
        self._field_size = 15
        self._current_position = current_point
        self._movieballs_count = movieballs_count
        self._moviemons = moviemons
        self._enemies_count = 15
        self._balls_treasures_count = 20
        self._captured_movies = []
        self._game_map: typing.Optional[list[list[int]]] = None
        self._player_strength = 1

    def dump(self, game_name="current"):
        GameManager.dump(self, game_name)

    def init_game_map(self):
        game_map = []
        for i in range(self._field_size):
            game_map.append([0 for _ in range(self._field_size)])
        y_pos, x_pos = self._current_position
        max_poke_count = self._max_pokeballs_count
        max_enemy_count = self._enemies_count
        for i, row in enumerate(game_map):
            for j, col in enumerate(row):
                if (i, j) == (y_pos, x_pos):
                    continue
                value = random.choices([0, 2, 3], [0.76, 0.1, 0.14])[0]
                if value == self.POKEBALL:
                    if max_poke_count <= 0:
                        value = self.MONSTER
                    max_poke_count -= 1
                if value == self.MONSTER:
                    if max_enemy_count <= 0:
                        continue
                    max_enemy_count -= 1

                game_map[i][j] = value
        enemy_count = 0
        poke_count = 0
        for row in game_map:
            for cell in row:
                if cell == self.MONSTER:
                    enemy_count += 1
                if cell == self.POKEBALL:
                    poke_count += 1
        self._game_map = game_map
        return

    def set_new_player_position(self, direction: str):
        y_pos, x_pos = self._current_position
        if direction == 'up':
            y_pos -= 1
        elif direction == 'left':
            x_pos -= 1
        elif direction == 'right':
            x_pos += 1
        elif direction == 'bottom':
            y_pos += 1
        else:
            return
        if not 0 <= x_pos < self._field_size:
            return
        if not 0 <= y_pos < self._field_size:
            return
        self._current_position = (y_pos, x_pos)

        return self.determine_action()

    def determine_action(self) -> dict:
        y_pos, x_pos = self._current_position
        if self._game_map[y_pos][x_pos] == self.MONSTER:
            return {"action": {"type": "monster", "monster_data": {'id': 1, 'strength': '2'},
                               'message': f'Monviemonster {"qwe"} found!<br>'
                                          f'{"Fight him!" if self._player_strength - 2 < 3 else "Run! Fly you fool!"}'}}
        if self._game_map[y_pos][x_pos] == self.POKEBALL:
            poke_count = random.randint(0, 20)
            self._movieballs_count += poke_count
            return {"action": {"type": "ball", 'count': poke_count, 'message': f'Found {poke_count} movieballs!'}}
        return {}

    def get_random_movie(self):
        pass

    def get_strength(self):
        pass

    def get_movie(self):
        pass

    def save_game(self, savefile_id: int):

        if savefile_id == 1:
            filename = "slotA_{captured}_{total}"
        elif savefile_id == 2:
            filename = "slotB_{captured}_{total}"
        elif savefile_id == 3:
            filename = "slotC_{captured}_{total}"
        else:
            return

        GameManager.dump(self, filename)

    def get_data_for_map(self):
        return {
            'map_data': {
                'player_strength': self._player_strength,
                'pokeballs': self._movieballs_count,
                'captured': f"{len(self._captured_movies)} / {self._enemies_count}",
                'field': self._game_map
            }
        }


class GameManager:

    def __init__(self, game=None):
        self._current_game = game

    def get_current_game(self) -> Game:
        if self._current_game is None:
            self._current_game = self.load()
        return self._current_game

    def set_current_game(self, game=None) -> None:
        if self._current_game is None and game is None:
            game = self.load()
        self._current_game = game

    @classmethod
    def load(cls, filename: str = "current"):
        filepath = os.path.join(django_settings.BASE_DIR, 'moviemon', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'wb'):
                pass
        with open(filepath, 'rb') as f:
            game_instance = pickle.load(f)
        return game_instance

    @classmethod
    def dump(cls, game: Game, filename="current") -> None:
        filepath = os.path.join(django_settings.BASE_DIR, 'moviemon', filename)
        with open(filepath, 'wb') as f:
            pickle.dump(game, f, protocol=pickle.HIGHEST_PROTOCOL)


game_storage = GameManager()


def start_new_game():
    game = Game((random.randint(0, 15), random.randint(0, 15)), 15, {})
    game.init_game_map()
    game_storage.set_current_game(game)
    game.dump()
    return game


if __name__ == '__main__':
    start_new_game()
