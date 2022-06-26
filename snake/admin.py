from django.contrib import admin

from .models import SnakeScore

# Register your models here.
class SnakeScoreAdmin(admin.ModelAdmin):
    list_display = ('score', 'user_name', 'user_hallway', 'date')
    list_filter = ['date', 'score']


admin.site.register(SnakeScore, SnakeScoreAdmin)
