from django.shortcuts import render
import typing
from .game import Game, game_storage, start_new_game


def title_screen(request):
    return render(request, "titlescreen.html", {
        'buttons': {'A': {'link': '/worldmap/new_game/', 'active': True},
                    'B': {'link': '/options/load_game/', 'active': True}},
        'title': 'Moviemon'
    })


def worldmap(request, direction: typing.Optional[str] = None):

    monster_id = False
    if request.method == "GET":
        # Start to create a new game for user
        if 'new_game' in request.path:
            start_new_game()

    current_game: Game = game_storage.get_current_game()

    action = {}
    if direction:
        action = current_game.set_new_player_position(direction)
        if not action:
            action = {}
        if action.get('action', {}).get('type') == 'monster':
            monster_id = action['action'].get('monster_id')
    map_data = current_game.get_data_for_map()
    map_data = {**map_data, **action}

    return render(request, "worldmap.html", {
        'buttons': {'A': {'link': f'/battle/{monster_id}', 'active': monster_id is not False},
                    'select': {'link': '/movindex'}, 'start': {'link': '/options'},
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
    return render(request, "options.html", {
        'buttons': {'A': {'link': '/options/save_game/', 'active': True, 'text': 'A - Save'},
                    'B': {'link': '/', 'active': True, 'text': 'B - Quit'},
                    'start': {'link': '/worldmap'}},
        'title': 'Options'
    })


def save(request):
    pass


def load(request):
    pass
