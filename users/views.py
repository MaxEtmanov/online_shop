from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.db import transaction
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Создаём пользователя
                user = form.save()
                user.email = form.cleaned_data.get('email')
                user.save()

                # Обновляем профиль
                profile = user.profile  # сигнал уже создал UserProfile
                profile.phone_number = form.cleaned_data.get('phone_number')
                profile.address = form.cleaned_data.get('address')
                profile.save()

                # Авторизуем пользователя
                login(request, user)
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    """
    Простой профиль пользователя.
    Показывает basic info + при необходимости можно расширить (редактирование, история и т.д.).
    """
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'users/profile.html', context)
