from django.shortcuts import render
import typing
from .game import Game, game_storage, start_new_game


def title_screen(request):
    return render(request, "titlescreen.html", {
        'buttons': {'A': {'link': '/worldmap/new_game/', 'active': True},
                    'B': {'link': '/options/load_game/', 'active': True}},
        'title': 'Moviemon'
    })


def worldmap(request, direction: typing.Optional[str] = None, new_game: bool = False):

    battle_active = False
    if request.method == "GET":
        # Start to create a new game for user
        if 'new_game' in request.path:
            print("start new game\n\n")
            start_new_game()

    current_game: Game = game_storage.get_current_game()

    action = {}
    if direction:
        current_game.set_new_player_position(direction)
        action = current_game.determine_action()
        if action.get('action', {}).get('type') == 'monster':
            battle_active = True
    map_data = current_game.get_data_for_map()
    map_data = {**map_data, **action}

    return render(request, "worldmap.html", {
        'buttons': {'A': {'link': '/worldmap', 'active': battle_active},
                    'select': {'link': '/movindex'}, 'start': {'link': '/option'},
                    'arrow_top': {'link': '/worldmap/up'}, 'arrow_left': {'link': '/worldmap/left'},
                    'arrow_right': {'link': '/worldmap/right'}, 'arrow_bottom': {'link': '/worldmap/bottom'},
                    },
        "title": "Catch em all",
        **map_data
    })


def battle(request, moviemon_id: int):
    pass


def moviedex(request):
    pass


def detail(request, moviemon: int):
    pass


def option(request):
    pass


def save(request):
    pass


def load(request):
    pass
