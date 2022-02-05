from django.shortcuts import render
from django.apps import apps

snake_game = None

def index(request):
    return render(request, 'snake/index.html', {})
