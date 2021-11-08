from django.apps import AppConfig
from ilcon.ilcon import Ilcon


class IlconConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ilcon'
    ilcon = None

    def ready(self):
        if not self.ilcon:
            self.ilcon = Ilcon()
