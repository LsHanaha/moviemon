from django.shortcuts import render
import typing
from .game import Game, start_new_game


def title_screen(request):
    return render(request, "titlescreen.html", {
        'buttons': {'A': {'link': '/worldmap', 'active': True}, 'B': {'link': '/options/load_game', 'active': True}},
        'title': 'Moviemon'
    })


def worldmap(request, direction: typing.Optional[str] = None):

    battle_active = False
    if request.method == "GET":
        # Start to create a new game for user
        game = start_new_game()

    return render(request, "worldmap.html", {
        'buttons': {'A': {'link': '/worldmap', 'active': battle_active},
                    'select': {'link': '/movindex'}, 'start': {'link': '/option'},
                    'arrow_top': {'link': '/worldmap/up'}, 'arrow_left': {'link': '/worldmap/left'},
                    'arrow_right': {'link': '/worldmap/right'}, 'arrow_bottom': {'link': '/worldmap/bottom'},
                    },
        "title": "Catch em all"
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
