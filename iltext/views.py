from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.decorators import login_required

from iltext.iltext import Iltext
from ilcon.waves import Waves
from iltext.stars import Stars

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
    else:
        background = None

        if waves:
            background = Waves(float(waves_bright))

        iltext = Iltext("    " + text, (255, 255, 255), background)
        ilcon.send(iltext)

    return HttpResponseRedirect(reverse('iltext:index'))

