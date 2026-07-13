from django.apps import AppConfig


class CryptoConfig(AppConfig):
    name = 'crypto'

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'