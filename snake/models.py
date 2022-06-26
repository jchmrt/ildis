from django.db import models

from datetime import datetime
from datetime import timedelta

def validate_condition(con):
    if not con:
        raise Exception()

class SnakeScore(models.Model):
    score = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=3, blank=True)
    user_hallway = models.PositiveSmallIntegerField(blank=True, null=True)

    def add_score(score, user_name, user_hallway):
        score = SnakeScore.validate_score(score)
        user_name = SnakeScore.validate_user_name(user_name)
        user_hallway = SnakeScore.validate_user_hallway(user_hallway)

        print("saving score")
        print(score)
        print(user_name)
        print(user_hallway)

        score = SnakeScore(score = score, user_name = user_name,
                           user_hallway = user_hallway)
        score.save()

        return score.pk

    def validate_score(score):
        validate_condition(isinstance(score, int))

        return max(score, 0)

    def validate_user_name(un):
        if un == '':
            return ''

        validate_condition(isinstance(un, str))
        validate_condition(len(un) <= 3)
        validate_condition(un.isalnum())
        
        return un.ljust(3, '_').upper()

    def validate_user_hallway(uh):
        if uh == '':
            return None

        uh = int(uh)
        validate_condition(isinstance(uh, int))
        validate_condition(uh <= 150 and uh >= 1)
            
        return uh

    def ranking(self):
        rs = Highscore.objects.filter(score__gt=self.score)
        return rs.aggregate(ranking=Count('score'))['ranking'] + 1

    def get_high_scores(n, time_limit=None):
        objs = SnakeScore.objects;
        if time_limit:
            objs = objs.filter(date__gte=time_limit)
        return SnakeScore.objects.order_by('-score')[:n]

    def get_daily_high_scores(n):
        return SnakeScore.get_high_scores(n, datetime.now() - timedelta(days=1))

    def get_weekly_high_scores(n):
        return SnakeScore.get_high_scores(n, datetime.now() - timedelta(weeks=1))

    def get_monthly_high_scores(n):
        return SnakeScore.get_high_scores(n, datetime.now() - timedelta(weeks=4))

    def get_yearly_high_scores(n):
        return SnakeScore.get_high_scores(n, datetime.now() - timedelta(days=365))
