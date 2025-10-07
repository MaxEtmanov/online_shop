from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        # Импортируем модуль signals при старте приложения,
        # чтобы декоратор @receiver зарегистрировал обработчик.
        # noqa: F401 нужен, чтобы linters не ругались на неиспользуемый импорт.
        import users.signals