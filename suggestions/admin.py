from django.contrib import admin

from .models import NYSuggestion

class NYSuggestionAdmin(admin.ModelAdmin):
    list_display = ('suggestion_text', 'sender_name', 'sender_hallway', 'submission_date', 'approved')
    list_filter = ['submission_date', 'approved']

# Register your models here.
admin.site.register(NYSuggestion, NYSuggestionAdmin)
