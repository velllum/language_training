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
        return context


class ShowWord(
    views.generic.DetailView, utils.AddReplayWordMixin, utils.TranslateContentMixin, utils.NavigatingPagesMixin
):
    """- Вывод слова"""
    template_name = "translator/show_word.html"
    slug_url_kwarg = 'word_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.translation
        context["all_count"] = self.model.objects.filter(
                                is_free=True, category__slug=self.kwargs.get("category_slug")
                            ).count()  # число всех данных из базы
        self.last_count = self.model.objects.filter(
                                is_free=True, pk__lte=self.object.pk, category__slug=self.kwargs.get("category_slug")
                            ).count()
        context["last_count"] = self.last_count  # число текущего номера в массиве из базы
        context["number_page"] = self.get_number_page  # число текущей страницы, для ссылки
        return context

    @property
    def get_number_page(self):
        return ((self.last_count - 1) // 10) + 1


class RepeatWords(views.generic.DetailView, utils.AddReplayWordAndNavigatingMixin):
    """- Повтор"""
    template_name = "translator/repeat_words.html"
    slug_url_kwarg = 'word_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Повтор слов"
        context["name_space"] = self.name_space
        return context


class ExtendReplay(views.generic.DetailView, utils.AddReplayWordAndNavigatingMixin, utils.TranslateContentMixin):
    """- Ответ, Продление повтора"""
    template_name = "translator/extend_replay.html"
    slug_url_kwarg = 'word_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Повтор слов"
        return context

    @property
    def get_url_kwargs(self):
        """- получить словарь kwargs"""
        if "word_slug" in self.kwargs:
            if not self.list_slugs:
                del self.kwargs["word_slug"]
            else:
                self.kwargs["word_slug"] = self.next_redirect_page  # переписать чтоб редирект вел на след страницу
            return self.kwargs

    @property
    def get_url_name(self):
        """- имя страницы редиректа"""
        if not self.list_slugs:
            return "word"
        return "repeat_words"

    @property
    def get_name_space(self):
        """- меняем русский контент на иностранный"""
        return "over"


class AudioReplay(views.generic.DetailView, utils.AddReplayWordAndNavigatingMixin, utils.TranslateContentMixin):
    """- Аудио повтор слов добавленных в закладки"""
    template_name = "translator/audio_replay.html"
    slug_url_kwarg = 'word_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Аудио повтор слов"
        return context

    @property
    def get_url_kwargs(self):
        """- переопределить словарь kwargs, при удалении первого слова"""
        if "word_slug" in self.kwargs:
            if not self.list_slugs:
                del self.kwargs["word_slug"]
            else:
                self.kwargs["word_slug"] = self.next_redirect_page
            return self.kwargs

    @property
    def get_url_name(self):
        """- имя страницы редиректа, если больше в списке слов не осталось"""
        if not self.list_slugs:
            return "word"
        return self.res.url_name


class Login(utils.BaseMixin):
    """- Авторизация"""
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form = forms.LoginForm(request.POST or None)

    def get(self, request, **kwargs):
        """- Отобразить форму на странице"""
        context = {
            "form": self.form,
            "title": "Авторизация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/auth.html", context)

    def post(self, request, **kwargs):
        """- Работа с данными от формы"""
        if self.form.is_valid():
            email = self.form.cleaned_data.get("email")
            password = self.form.cleaned_data.get("password")
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect(reverse(f"{self.res.namespace}:word", kwargs={"category_slug": kwargs.get("category_slug")}))
        context = {
            "form": self.form,
            "title": "Авторизация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/auth.html", context)


class Register(utils.BaseMixin):
    """- Регистрация"""
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form = forms.RegisterForm(request.POST or None)

    def get(self, request, **kwargs):
        """- Отобразить форму на странице"""
        context = {
            "form": self.form,
            "title": "Регистрация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/register.html", context)

    def post(self, request, **kwargs):
        """- Работа с данными от формы"""
        if self.form.is_valid():
            new_password = User.objects.make_random_password(length=10)
            new_email = self.form.cleaned_data.get("email")
            new_user_name = str(self.form.cleaned_data.get("email")).replace("@", "_")
            new_user = self.form.save(commit=False)
            new_user.username = new_user_name
            new_user.email = new_email
            new_user.save()
            new_user.set_password(new_password)
            new_user.save()
            self.create_mail(new_email, new_password)
            user = authenticate(username=new_user_name, password=new_password)
            login(request, user)
            return redirect(reverse(f"{self.res.namespace}:word", kwargs={"category_slug": kwargs.get("category_slug")}))
        context = {
            "form": self.form,
            "title": "Регистрация",
            'category_slug': kwargs.get("category_slug"),
        }
        return render(request, "translator/register.html", context)

    @staticmethod
    def create_mail(email, pas):
        """- Создание почты"""
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


def settings(request, category_slug):
    """- Настойки"""
    return render(request, "translator/settings.html", context={"category_slug": category_slug})
