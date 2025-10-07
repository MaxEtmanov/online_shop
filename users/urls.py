from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # /accounts/signup/
    path('profile/', views.profile, name='profile'),
]