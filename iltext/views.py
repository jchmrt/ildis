from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.decorators import login_required

from iltext.flash_text import FlashText
from ilcon.waves import Waves


@login_required
def index(request):
    return render(request, 'iltext/index.html', {})


@login_required
def send(request):
    text = request.POST['text']
    waves = 'waves' in request.POST
    waves_bright = request.POST['waves-bright']

    ilcon = apps.get_app_config('ilcon').ilcon

    if text == "" and not waves:
        ilcon.clear()
    elif text == "s":
        ilcon.send(Stars())
    elif text == "n":
        ilcon.send(NYE())
    elif text == "t":
        ilcon.send(ObjectsRenderer(TimeMessageBuilder()))
    elif text == "f":
        ilcon.send(Fire())
    else:
        background = None

        if waves:
            background = Waves(float(waves_bright))

        iltext = FlashText("    " + text, color=(255, 255, 255),
                           background=background)
        ilcon.send(iltext)

    return HttpResponseRedirect(reverse('iltext:index'))
