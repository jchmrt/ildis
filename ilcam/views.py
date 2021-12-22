from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps

from base64 import b64decode
from PIL import Image
import io

from iltext.iltext import Iltext
from ilcon.waves import Waves
from ilcam.ilimg import Ilimg


@login_required
def index(request):
    return render(request, 'ilcam/index.html', {})

@login_required
def send(request):
    data_url = request.POST['image']
    header, encoded = data_url.split(",", 1)
    data = b64decode(encoded)

    image = Image.open(io.BytesIO(data))
    pixels = image.load()

    ilcon = apps.get_app_config('ilcon').ilcon

    ilcon.send(Ilimg(pixels))

    return HttpResponse("success")
    
