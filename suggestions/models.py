from django.db import models


class NYSuggestion(models.Model):
    suggestion_text = models.CharField(max_length=200)
    sender_name = models.CharField(max_length=100)
    sender_hallway = models.PositiveSmallIntegerField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.suggestion_text
