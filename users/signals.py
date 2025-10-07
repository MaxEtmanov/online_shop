from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.apps import apps

# Используем пост-сейв сигнал для модели пользователя, заданной в AUTH_USER_MODEL
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Когда пользователь создаётся (created=True) — создаём связанный UserProfile.
    Мы используем apps.get_model, чтобы избежать циклических импортов, если потребуется.
    """
    if not created:
        # Если пользователь уже существовал — ничего не делаем
        return

    # Импорт модели профиля "лениво" через apps.get_model, чтобы не было циклических импортов
    UserProfile = apps.get_model('users', 'UserProfile')

    # Создаём профиль, если он по каким-то причинам ещё не существует
    # get_or_create — защищает от дублирования (на всякий случай)
    UserProfile.objects.get_or_create(user=instance)