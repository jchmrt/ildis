from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

@login_required
def index(request):
    return render(request, 'ilbright/index.html', {})

@login_required
def send(request):
    ilcon = apps.get_app_config('ilcon').ilcon

    try:
        brightness = request.POST['brightness']
        bright_int = int(brightness)
        if bright_int >= 0 and bright_int < 255:
            ilcon.set_brightness(bright_int)
    except:
        pass

    return HttpResponseRedirect(reverse('ilbright:index'))
