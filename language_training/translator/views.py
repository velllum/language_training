from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from django import views

from django.conf import settings as sett

from . import models
from . import utils
from . import forms


class Category(views.generic.ListView):
    """- Вывод категорий"""
    model = models.Category
    template_name = "translator/category.html"
    context_object_name = "categories"
    allow_empty = False

    def get_queryset(self):
        return models.Category.objects.all()

    def get_context_data(self,  *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Категории"
        return context


class Word(utils.TranslateContentMixin, views.generic.ListView):
    """- Вывод списка слов"""
    paginate_by = sett.NUMBER_PAGES
    template_name = "translator/words.html"
    context_object_name = "words_list"

    def get_queryset(self):
        query = self.model.objects.filter(category__slug=self.kwargs.get("category_slug")).select_related('category')
        is_free = query.filter(is_free=True)
        if is_free:
            return is_free
        return query[:sett.NUMBER_PAGES]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список слов"
        context["category_slug"] = self.kwargs.get("category_slug")
        print(self.request.content_params)
        return context


class ShowWord(views.generic.DetailView, utils.TranslateContentMixin, utils.NavigatingPagesMixin):
    """- Вывод слова"""
    template_name = "translator/show_word.html"
    slug_url_kwarg = 'word_slug'

    def get_queryset(self):
        query = self.model.objects.filter(
            category__slug=self.kwargs.get("category_slug"),
            slug=self.kwargs.get("word_slug"),
        ).select_related('category')
        if query:
            return query

    def get_object(self, **kwargs):
        print("get_object", self.kwargs)
        return super().get_object(**kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_slug"] = self.kwargs.get("category_slug")
        context["title"] = self.object.translation
        context["all_count"] = self.model.objects.filter(
                                is_free=True, category__slug=self.kwargs.get("category_slug")
                            ).count()
        last_count = self.model.objects.filter(
                                is_free=True, pk__lte=self.object.pk, category__slug=self.kwargs.get("category_slug")
                            ).count()
        context["last_count"] = last_count
        context["number_page"] = ((last_count - 1) // 10) + 1
        return context


class AudioReplay(utils.TranslateContentMixin, views.generic.ListView):
    """- Аудио повтор слов добавленных в закладки"""
    template_name = "translator/audio_replay.html"

    def get_queryset(self):
        query = self.model.objects.filter(category__slug=self.kwargs.get("category_slug")).select_related('category')
        if query:
            return query.select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_slug"] = self.kwargs.get("category_slug")
        context["title"] = "Аудио повтор"
        return context


class ExtendReplay(utils.TranslateContentMixin, views.generic.ListView):
    """- Продление повтора"""
    template_name = "translator/extend_replay.html"

    def get_queryset(self):
        query = self.model.objects.filter(category__slug=self.kwargs.get("category_slug")).select_related('category')
        if query:
            return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_slug"] = self.kwargs.get("category_slug")
        context["title"] = "Добавить слово в повтор"
        return context


class Login(views.generic.View):
    """- Авторизация"""
    def get(self, request, **kwargs):
        """- Отобразить форму на странице"""
        form = forms.LoginForm(request.POST or None)
        context = {
            "form": form,
            "title": "Авторизация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/auth.html", context)

    def post(self, request, **kwargs):
        """- Работа с данными от формы"""
        res = resolve(request.path)
        form = forms.LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect(reverse(f"{res.namespace}:word", kwargs={"category_slug": kwargs.get("category_slug")}))
        context = {
            "form": form,
            "title": "Авторизация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/auth.html", context)


class Register(views.View):
    """- Регистрация"""
    def get(self, request, **kwargs):
        """- Отобразить форму на странице"""
        form = forms.RegisterForm(request.POST or None)
        context = {
            "form": form,
            "title": "Регистрация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/register.html", context)

    def post(self, request, **kwargs):
        """- Работа с данными от формы"""
        res = resolve(request.path)
        form = forms.RegisterForm(request.POST or None)
        if form.is_valid():

            new_password = User.objects.make_random_password(length=10)
            new_email = form.cleaned_data.get("email")
            # superusers_emails = User.objects.filter(is_superuser=True).values_list('email')
            new_user = form.save(commit=False)
            new_user.username = str(form.cleaned_data.get("email")).replace("@", "_")
            new_user.email = new_email
            new_user.save()
            new_user.set_password(new_password)
            new_user.save()
            self.sending_mail(new_email, new_password)
            user = authenticate(
                username=str(form.cleaned_data.get("email")).replace("@", "_"),
                password=new_password,
            )
            login(request, user)
            return redirect(reverse(f"{res.namespace}:word", kwargs={"category_slug": kwargs.get("category_slug")}))
        context = {
            "form": form,
            "title": "Регистрация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/register.html", context)

    @staticmethod
    def sending_mail(email, pas):
        subject = 'Регистрация на сайте'
        message = f'Логи: {email}, пароль: {pas}'
        send_mail(subject, message, sett.EMAIL_HOST_USER, [email], fail_silently=False,)


def search(request, category_slug):
    """- Поиск"""
    q = str(request.GET.get('q')).strip()
    res = resolve(request.path)
    if q:
        queryset = models.Word.objects.filter(category__slug=category_slug).filter(
            Q(translation__icontains=q) | Q(word__icontains=q)
        ).first()
        if queryset:
            return redirect(reverse(f"{res.namespace}:card", kwargs={
                "category_slug": category_slug, "word_slug": queryset.slug
            }))
    return redirect(reverse(f"{res.namespace}:word", kwargs={"category_slug": category_slug}))


def logout_user(request, category_slug):
    """- выход пользователя на сайте"""
    logout(request)
    res = resolve(request.path)
    return redirect(reverse(f"{res.namespace}:word", kwargs={"category_slug": category_slug}))


def repeat_words(request, category_slug):
    """- Повторение слов добавленных в закладки"""
    return render(request, "translator/repeat_words.html", context={"category_slug": category_slug})


def audio_replay(request, category_slug):
    """- Аудио повтор слов добавленных в закладки"""
    return render(request, "translator/audio_replay.html", context={"category_slug": category_slug})


def extend_replay(request, category_slug):
    """- Продление повтора"""
    return render(request, "translator/extend_replay.html", context={"category_slug": category_slug})


def settings(request, category_slug):
    """- Настойки"""
    return render(request, "translator/settings.html", context={"category_slug": category_slug})
