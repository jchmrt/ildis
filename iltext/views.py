from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps

from iltext.iltext import Iltext
from ilcon.waves import Waves

# Create your views here.
def index(request):
    return render(request, 'iltext/index.html', {})

def send(request):
    iltext = Iltext(request.POST['text'])
    ilcon = apps.get_app_config('ilcon').ilcon

    ilcon.send(iltext)

    return HttpResponseRedirect(reverse('iltext:index'))

