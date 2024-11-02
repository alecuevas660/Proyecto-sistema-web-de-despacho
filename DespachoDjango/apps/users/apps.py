from django.apps import AppConfig

class UsersConfig(AppConfig):  # Cambiado de UseraccountConfig a UsersConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Usuarios'
