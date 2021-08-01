from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse, resolve
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

    def get_context_data(self,  *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Категории"
        return context


class Word(utils.TranslateContentMixin, ListView):
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


class ShowWord(DetailView, utils.TranslateContentMixin, utils.NavigatingPagesMixin):
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


class AudioReplay(utils.TranslateContentMixin, ListView):
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


class ExtendReplay(utils.TranslateContentMixin, ListView):
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


class Register(CreateView):
    """- Регистрация"""
    form_class = forms.RegisterUserForm
    template_name = "translator/register.html"
    success_url = reverse_lazy("url_translator:auth")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        context["category_slug"] = self.kwargs.get("category_slug")
        return context


def search(request, category_slug):
    """- Поиск"""
    q = str(request.GET.get('q')).strip()
    res = resolve(request.path)
    if q:
        queryset = models.Word.objects.filter(category__slug=category_slug).filter(
            Q(translation__icontains=q) | Q(word__icontains=q)
        ).first()
        if queryset:
            return redirect(reverse(f"{res.namespace}:card", args=(category_slug, queryset.slug)))
    return redirect(reverse(f"{res.namespace}:word", args=(category_slug,)))


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


def auth(request, category_slug):
    """- Авторизация"""
    return render(request, "translator/auth.html", context={"category_slug": category_slug})

