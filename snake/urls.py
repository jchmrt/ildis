from django.urls import path

from . import views

app_name = 'snake'
urlpatterns = [
    path('', views.index, name='index'),
    path('scores', views.get_high_scores, name='scores')
]
