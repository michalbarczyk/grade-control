from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'system'

    def ready(self):
        import system.signals
