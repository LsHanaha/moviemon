from django.shortcuts import render


def title_screen(request):
    return render(request, "titlescreen.html", {
        'buttons': {'A': {'link': '/worldmap', 'active': True}, 'B': {'link': '/options/load_game', 'active': True}},
        'title': 'Moviemon'
    })


def worldmap(request):
    pass


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
