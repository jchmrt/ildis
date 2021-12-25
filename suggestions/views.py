from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import NYSuggestion

def index(request):
    return render(request, 'suggestions/index.html', {})

def send(request):
    message = request.POST['suggestion-text']
    sender = request.POST['suggestion-sender']
    hallway_str = request.POST['suggestion-hallway']
    hallway_number = None

    try:
        hallway_number = int(hallway_str)
    except ValueError:
        pass


    suggestion = NYSuggestion(suggestion_text=message,
                              sender_name = sender,
                              sender_hallway = hallway_number)
    suggestion.save()

    messages.success(request, """Successfully submitted your message!""")
    return HttpResponseRedirect(reverse('suggestions:index'))
