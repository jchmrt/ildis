from django.shortcuts import render
from django.apps import apps
from django.http import JsonResponse
from django.core import serializers

from .models import SnakeScore


def index(request):
    return render(request, 'snake/index.html', {})

def get_high_scores(request):
    n = 10

    all_scores = SnakeScore.get_high_scores(n)
    yearly_scores = SnakeScore.get_yearly_high_scores(n)
    monthly_scores = SnakeScore.get_monthly_high_scores(n)
    weekly_scores = SnakeScore.get_weekly_high_scores(n)
    daily_scores = SnakeScore.get_daily_high_scores(n)

    def ser(data):
        return list(data.values())

    scores = {
        "all_time": ser(all_scores),
        "yearly": ser(yearly_scores),
        "monthly": ser(monthly_scores),
        "weekly": ser(weekly_scores),
        "daily": ser(daily_scores),
    }


    return JsonResponse(scores)
