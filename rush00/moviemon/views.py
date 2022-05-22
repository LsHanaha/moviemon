from django.shortcuts import render
import typing
from .game import Game, game_storage, start_new_game
import random


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
                    'select': {'link': '/movindex'}, 'start': {'link': '/option'},
                    'arrow_top': {'link': '/worldmap/up'}, 'arrow_left': {'link': '/worldmap/left'},
                    'arrow_right': {'link': '/worldmap/right'}, 'arrow_bottom': {'link': '/worldmap/bottom'},
                    },
        "title": "Catch em all",
        **map_data
    })


def battle(request, moviemon_id: str):
    current_game: Game = game_storage.get_current_game()
    moviemon = current_game._moviemons[moviemon_id]
    luck = 50 - moviemon["imdbRating"] * 10 + current_game._player_strength * 5
    check = 1
    if luck < 1:
        luck = 1
    elif luck > 90:
        luck = 90
    if 'throw' in request.path:
        if current_game._movieballs_count > 0:
            if random.randint(0, 100) > luck:
                battle_text = "Throw Failed! Try again!"
                current_game._movieballs_count -= 1
            else:
                battle_text = f"Congrats, You catched {moviemon['Title']}! Press B to return to Worldmap!"
                current_game._captured_movies.append(moviemon)
                check = 0
        else:
            battle_text = "Oooops! You're out of movieballs! Press B to return to Worldmap!"
            check = 0
    else:
        battle_text = f'{moviemon["Title"]} appeared!'
    game_dict = {**moviemon, 'Luck': luck, 'Movieballs': current_game._movieballs_count, 'Battle_Text': battle_text, 'buttons': {'B': {'link': '/worldmap', 'active': True}}}
    if check:
        game_dict['buttons']['A'] = {'link': f'/battle/{moviemon_id}/throw', 'active': True}
    return render(request, 'battle.html', game_dict)


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
