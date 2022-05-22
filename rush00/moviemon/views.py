from django.shortcuts import render, redirect
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
                    'select': {'link': '/moviedex'}, 'start': {'link': '/options'},
                    'arrow_top': {'link': '/worldmap/up'}, 'arrow_left': {'link': '/worldmap/left'},
                    'arrow_right': {'link': '/worldmap/right'}, 'arrow_bottom': {'link': '/worldmap/bottom'},
                    },
        "title": "Catch em all",
        **map_data
    })


def battle(request, moviemon_id: str):
    pass


def moviedex(request):
    direction = None

    current_game = game_storage.get_current_game()
    if request.method == "GET" and request.GET:
        direction = request.GET.get("direction")
    else:
        current_game.moviedex_current = 0

    try:
        selected_pos = current_game.moviedex_current
    except AttributeError:
        current_game.moviedex_current = 0
        selected_pos = 0

    captured_movies = current_game.get_captured_movies()

    if direction == 'down' and selected_pos < len(captured_movies) - 1:
        selected_pos += 1
        current_game.moviedex_current = selected_pos
    if direction == 'up' and selected_pos > 0:
        selected_pos -= 1
        current_game.moviedex_current = selected_pos
    selected_id = current_game.get_movie_id_by_pos(selected_pos)
    movies_to_show = current_game.get_selected_previous_and_next_movie(selected_pos)

    return render(request, "moviedex.html", {
        'buttons': {'A': {'link': f'/detai/{selected_id}/', 'active': True},
                    'select': {'link': '/worldmap'},
                    'arrow_top': {'link': '/moviedex/up'},
                    'arrow_bottom': {'link': '/moviedex/down'}
                    },
        'title': 'Moviedex',
        'captured_movies': movies_to_show,
        'selected_movie_id': selected_id
    })


def detail(request, moviemon: str):
    if moviemon in ['up', 'down']:
        return redirect(f'/moviedex?direction={moviemon}')
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
