from django.apps import AppConfig


class merkleTreeConfig(AppConfig):
    name = 'merkleTree'
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import merkleTree.signals