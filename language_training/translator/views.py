from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.conf import settings as sett

from . import models
from . import utils
from . import forms


class Category(ListView):
    """- Вывод категорий"""
    model = models.Category
    template_name = "translator/category.html"
    context_object_name = "categories"
    allow_empty = False

    def get_queryset(self):
        return models.Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Категории"
        return context


class Word(utils.WordMixin, ListView):
    """- Вывод списка слов"""
    paginate_by = sett.NUMBER_PAGES
    template_name = "translator/words.html"
    context_object_name = "page_words"

    def get_queryset(self):
        query = models.Word.objects.filter(category__slug=self.kwargs['category_slug'])
        query_is_free = query.filter(is_free=True)
        if query_is_free:
            return query_is_free
        return query[:sett.NUMBER_PAGES]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список слов"
        context["category_slug"] = self.kwargs['category_slug']
        return context


class ShowWord(utils.WordMixin, DetailView):
    """- Вывод слова"""
    template_name = "translator/show_word.html"
    context_object_name = "word"
    slug_url_kwarg = 'word_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_slug"] = self.kwargs['category_slug']
        context["title"] = self.object.translation
        context["previous"] = models.Word.objects.filter(is_free=True, id__lt=self.object.id).last()
        context["next"] = models.Word.objects.filter(is_free=True, id__gt=self.object.id).first()
        context["all_count"] = models.Word.objects.filter(is_free=True).count()
        context["last_count"] = models.Word.objects.filter(is_free=True, id__lte=self.object.id).count()
        return context


class Register(utils.WordMixin, CreateView):
    """- Регистрация"""
    form_class = forms.RegisterUserForm
    template_name = "translator/register.html"
    success_url = reverse_lazy("auth")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        context["category_slug"] = self.kwargs['category_slug']
        return context






def audio_replay(request, category_slug):
    """- Аудио повтор слов добавленных в закладки"""
    return render(request, "translator/audio_replay.html", context={"category_slug": category_slug})


def repeat_words(request, category_slug):
    """- Повторение слов добавленных в закладки"""
    return render(request, "translator/repeat_words.html", context={"category_slug": category_slug})


def extend_replay(request, category_slug):
    """- Продление повтора"""
    return render(request, "translator/extend_replay.html", context={"category_slug": category_slug})


def settings(request, category_slug):
    """- Настойки"""
    return render(request, "translator/settings.html", context={"category_slug": category_slug})


def auth(request, category_slug):
    """- Авторизация"""
    return render(request, "translator/auth.html", context={"category_slug": category_slug})


