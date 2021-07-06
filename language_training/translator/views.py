from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings as sett

from . import models
from . import utils


class Category(ListView):
    """- Вывод категорий"""
    model = models.Category
    template_name = "translator/category.html"
    context_object_name = "categories"
    allow_empty = False

    def get_queryset(self):
        return models.Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Category, self).get_context_data(**kwargs)
        context["title"] = "Категории"
        return context


class Word(utils.WordMixin, ListView):
    """- Вывод списка слов"""
    paginate_by = sett.NUMBER_PAGES
    template_name = "translator/words.html"
    context_object_name = "page_words"

    def get_queryset(self):
        query = models.Word.objects.filter(category__slug=self.kwargs['category_slug']).order_by('-id')
        query_is_free = query.filter(is_free=True)
        if query_is_free:
            return query_is_free
        return query[:sett.NUMBER_PAGES]

    def get_context_data(self, **kwargs):
        context = super(Word, self).get_context_data(**kwargs)
        mixin_context = self.get_mixin_context(title="Список слов", category_slug=self.kwargs['category_slug'])
        context = dict(list(context.items()) + list(mixin_context.items()))
        return context


class ShowWord(utils.WordMixin, DetailView):
    """- Вывод слова"""
    template_name = "translator/show_word.html"
    context_object_name = "word"
    slug_url_kwarg = 'word_slug'

    def get_context_data(self, **kwargs):
        context = super(ShowWord, self).get_context_data(**kwargs)
        mixin_context = self.get_mixin_context(title=self.object.translation, category_slug=self.kwargs['category_slug'])
        context = dict(list(context.items()) + list(mixin_context.items()))
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


def register(request, category_slug):
    """- Регистрация"""
    return render(request, "translator/register.html", context={"category_slug": category_slug})

