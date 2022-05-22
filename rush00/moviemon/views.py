from django.shortcuts import render, redirect
from django.conf import settings as django_settings
import typing
from .game import Game, game_storage, start_new_game
import os


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
        'buttons': {'A': {'link': f'/moviedex/{selected_id}', 'active': True},
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
    current_game = game_storage.get_current_game()
    movie = current_game.get_movie(moviemon)
    return render(request, 'detail.html', {
        'buttons': {'B': {'link': '/moviedex', 'active': True}},
        'title': 'Detail',
        'movie': movie
    })


def option(request):
    return render(request, "options.html", {
        'buttons': {'A': {'link': '/options/save_game/', 'active': True, 'text': 'A - Save'},
                    'B': {'link': '/', 'active': True, 'text': 'B - Quit'},
                    'start': {'link': '/worldmap'}},
        'title': 'Options'
    })


def save(request):
    # return render(request, "options.html", {
    #     'buttons': {'A': {'link': '/options/save_game/', 'active': True, 'text': 'A - Save'},
    #                 'B': {'link': '/', 'active': True, 'text': 'B - Quit'},
    #                 'start': {'link': '/worldmap'}},
    #     'title': 'Options'
    # })
    pass


def load(request, save_file_name: str = None):

    current_game = game_storage.get_current_game()
    if request.method == 'GET' and save_file_name is None:
        current_game.selected_pos = 0

    try:
        current_game.selected_pos
    except AttributeError:
        current_game.selected_pos = 0

    if save_file_name == 'up' and current_game.selected_pos > 0:
        current_game.selected_pos -= 1
    elif save_file_name == 'down' and current_game.selected_pos < 2:
        current_game.selected_pos += 1

    arrow_buttons_status = True

    folder = os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves')
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    saves = [None, None, None]
    for file in files:
        file_ = file.split('/')[-1]
        if file_.startswith('slotA'):
            score = file_.split('_')[1].split('.')[0]
            saves[0] = {'filename': file_, 'name': f'Slot A: {score}'}
        elif file_.startswith('slotB'):
            score = file_.split('_')[1].split('.')[0]
            saves[1] = {'filename': file_, 'name': f'Slot B: {score}'}
        elif file_.startswith('slotC'):
            score = file_.split('_')[1].split('.')[0]
            saves[2] = {'filename': file_, 'name': f'Slot C: {score}'}

    load_target = saves[current_game.selected_pos]['filename'] if saves[current_game.selected_pos] else "#"
    load_link = f"/options/load_game/{load_target}"

    a_text = " Load"
    if request.method == 'POST' and save_file_name not in ['#', 'up', 'down']:
        game = game_storage.load(os.path.join('saves', save_file_name))
        game_storage.set_current_game(game)
        load_link = '/worldmap'
        arrow_buttons_status = False
        a_text = "Start Game"

    return render(request, "load.html", {
        'buttons': {'A': {'link': load_link, 'active': True, 'method': 'post', 'text': a_text},
                    'B': {'link': '/', 'active': arrow_buttons_status},
                    'arrow_top': {'link': '/options/load_game/up', 'active': arrow_buttons_status},
                    'arrow_bottom': {'link': '/options/load_game/down', 'active': arrow_buttons_status}
                    },
        'title': 'Options',
        'savefiles': saves,
        'selected_file_pos': current_game.selected_pos
    })
