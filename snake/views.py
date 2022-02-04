from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.decorators import login_required

from iltext.iltext import Iltext
from ilcon.waves import Waves
from iltext.stars import Stars
from suggestions.nye import NYE, ObjectsRenderer, TimeMessageBuilder
from snake.snake import SnakeGameWrapper, Direction

snake_game = None

def index(request):
    global snake_game
    ilcon = apps.get_app_config('ilcon').ilcon
    if not snake_game:
        snake_game = SnakeGameWrapper()
    ilcon.send(snake_game)
    return render(request, 'snake/index.html', {})

def send(request):
    d = request.POST["direction"]

    if d == "n":
        d = Direction.NORTH
    elif d == "s":
        d = Direction.SOUTH
    elif d == "w":
        d = Direction.WEST
    elif d == "e":
        d = Direction.EAST

    snake_game.put(d)

    return HttpResponseRedirect(reverse('snake:index'))

