from django.apps import AppConfig


class ShahzodspaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shahzodspace'

    def ready(self):
        import shahzodspace.signals