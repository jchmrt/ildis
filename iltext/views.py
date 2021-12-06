from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.decorators import login_required

from iltext.iltext import Iltext
from ilcon.waves import Waves

@login_required
def index(request):
    return render(request, 'iltext/index.html', {})

@login_required
def send(request):
    iltext = Iltext("              " + request.POST['text'])
    ilcon = apps.get_app_config('ilcon').ilcon

    if request.POST['text'] == "":
        ilcon.send(Waves())
    else:
        ilcon.send(iltext)

    return HttpResponseRedirect(reverse('iltext:index'))

