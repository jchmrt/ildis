from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.decorators import login_required

from ilcon.waves import Waves
from specials.stars import Stars
from specials.fire import Fire
from specials.christmas import GreenRed, Snow, ChristmasTree
from specials.time import TimePortrait
from suggestions.nye import NYE, ObjectsRenderer, TimeMessageBuilder, Fireworks

SPECIALS = [
    ("fire", "Fire", Fire),
    ("stars", "Stars", Stars),
    ("time", "Time", lambda: ObjectsRenderer(TimeMessageBuilder())),
    ("nye", "NYE", NYE),
    ("fireworks", "Fireworks", Fireworks),
    ("greenred", "Green Red", GreenRed),
    ("snow", "Snow", Snow),
    ("christmastree", "Christmas Tree", ChristmasTree),
    ("christmassnow", "Christmas Snow", lambda: ChristmasTree(Snow())),
    ("timeportrait", "Time Portrait", TimePortrait),
    ("timeportraitwaves", "Time Portrait Waves", lambda: TimePortrait(Waves(0.4))),
]


@login_required
def index(request):
    return render(request, 'specials/index.html', {"specials": SPECIALS})


@login_required
def send(request):
    special = request.POST['special']
    ilcon = apps.get_app_config('ilcon').ilcon

    for option in SPECIALS:
        if option[0] == special:
            ilcon.send(option[2]())
            break

    return HttpResponseRedirect(reverse('specials:index'))
