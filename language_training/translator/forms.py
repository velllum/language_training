from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from . import models

User = get_user_model()


class RepetitionWordsForm(forms.ModelForm):
    """- Скрытое поле, передача pk слова для добавление в сессию"""

    class Meta:
        model = models.Word
        fields = ('word_id',)

    word_id = forms.CharField(widget=forms.HiddenInput(), required=False)


class LoginForm(forms.ModelForm):
    """- Форма авторизации"""

    use_required_attribute = False
    default_errors = {
        'invalid': 'Введите правильный адрес почты.',
    }

    email = forms.EmailField(
        initial='',
        error_messages=default_errors,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'})
    )

    password = forms.CharField(
        initial='',
        widget=forms.PasswordInput(
            render_value=True, attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    def clean_email(self):
        """- проверка почты на валидность"""

        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).first():
            raise forms.ValidationError("Почтовый адрес не найден.")
        return email

    def clean_password(self):
        """- проверка пароля на валидность"""

        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email)
        for u in user:
            if not check_password(password, u.password):
                raise forms.ValidationError("Не верный пароль")
        return password

    class Meta:
        model = User
        fields = ('email', 'password')


class RegisterForm(forms.ModelForm):
    """- Форма регистрации"""

    use_required_attribute = False
    default_errors = {
        'invalid': 'Введите правильный адрес почты.',
    }

    email = forms.EmailField(
        error_messages=default_errors,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Почта'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Почтовый адрес зарегистрирован")
        return email

    class Meta:
        model = User
        fields = ('email',)
