from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    use_required_attribute = False
    default_errors = {
        # 'required': 'required',
        'invalid': 'Введите правильный адрес почты.',
        'max_length': 3,
        'min_length': 3,
    }

    email = forms.EmailField(error_messages=default_errors, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': "off"}))
    password1 = forms.CharField(error_messages=default_errors, label='Пароль', widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Пароль', 'autocomplete': "off"}))
    password2 = forms.CharField(error_messages=default_errors, label='Повтор пароля', widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Повтор пароля', 'autocomplete': "off"}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


