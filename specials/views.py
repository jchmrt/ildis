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
    ( False, "mirror", "Mirror", lambda: do_mirror()),
    ( True, "fire", "Fire", Fire),
    ( True, "stars", "Stars", Stars),
    ( True, "time", "Time", lambda: ObjectsRenderer(TimeMessageBuilder())),
    ( True, "nye", "NYE", NYE),
    ( True, "fireworks", "Fireworks", Fireworks),
    ( True, "greenred", "Green Red", GreenRed),
    ( True, "snow", "Snow", Snow),
    ( True, "christmastree", "Christmas Tree", ChristmasTree),
    ( True, "christmassnow", "Christmas Snow", lambda: ChristmasTree(Snow())),
    ( True, "timeportrait", "Time Portrait", TimePortrait),
    ( True, "timeportraitwaves", "Time Portrait Waves", lambda: TimePortrait(Waves(0.4))),
]


@login_required
def index(request):
    return render(request, 'specials/index.html', {"specials": SPECIALS})


@login_required
def send(request):
    special = request.POST['special']
    ilcon = apps.get_app_config('ilcon').ilcon

    for option in SPECIALS:
        if option[1] == special:

            # special is a Disp which will run longer:
            if option[0]:
                ilcon.send(option[3]())
            # special is a quick function:
            else:
                option[3]()

            break

    return HttpResponseRedirect(reverse('specials:index'))

def do_mirror():
    ilcon = apps.get_app_config('ilcon').ilcon

    ilcon.send_mirror()

