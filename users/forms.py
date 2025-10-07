from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Обязательный адрес электронной почты')
    phone_number = forms.CharField(required=False, max_length=20, label='Телефон')
    address = forms.CharField(required=False, max_length=255, label='Адрес')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')