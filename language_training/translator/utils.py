import datetime

from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.views import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from . import models
from . import forms


class BaseMixin(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = models.Word
        self.name_space = "rus"
        self.rus_ns = "rus"
        self.over_ns = "over"
        self.allow_empty = False
        self.object_list = None
        self.last_count = None
        self.list_slugs = None
        self.object = None
        self.form = None
        self.res = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form = forms.RepetitionWordsForm(request.POST or None)
        self.res = resolve(request.path)


class TranslateContentMixin(BaseMixin, BaseListView):
    """- Ссылка перевода контента"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["get_url_translate"] = self.get_url_translate()
        context["name_space"] = self.get_name_space
        return context

    def get_url_translate(self):
        """- Ссылка для кнопки перевода контента"""
        res = resolve(self.request.path)
        if "rus" not in res.namespace:
            namespace = self.rus_ns
        else:
            namespace = self.over_ns
        return reverse(viewname=f"{namespace}:{res.url_name}", kwargs=res.kwargs)

    @property
    def get_name_space(self):
        return self.name_space


class NavigatingPagesMixin(BaseMixin, BaseDetailView):
    """- Навигация по предыдущей и следующей страницей"""
    def get_context_data(self, **kwargs):
        kwargs["previous"] = self.get_url_page("pk__lt")
        kwargs["next"] = self.get_url_page("pk__gt")
        return kwargs

    def get_url_page(self, pk__):
        """- Получить ссылку следующей и новой статьи"""
        query = self.model.objects.filter(
            **{pk__: self.object.pk},
            is_free=True,
            category__slug=self.kwargs['category_slug'],
        )
        if not query:
            return None
        if pk__ is "pk__lt":
            query = query.order_by("-pk").first()
        else:
            query = query.first()
        res = resolve(self.request.path)
        if res.kwargs.get("word_slug"):
            res.kwargs["word_slug"] = query.slug
        return reverse(viewname=res.view_name, kwargs=res.kwargs)


class RepetitionWordsMixin(BaseMixin, BaseDetailView):
    """- Добавить, удалить слова из повтора"""
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.list_slugs = self.get_session_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_hidden"] = self.form
        context["list_slugs"] = self.list_slugs
        return context

    @property
    def get_session_data(self):
        """- получить данные из сессии"""
        repeat_words = self.request.session.get("repeat_words", None)
        if repeat_words:
            return [slug for slug, _ in repeat_words]
        else:
            return self.request.session.setdefault('repeat_words', list())

    @property
    def get_url_kwargs(self):
        """- переопределить словарь kwargs"""
        return self.kwargs

    @property
    def get_url_name(self):
        """- имя страницы редиректа"""
        return self.res.url_name

    def post(self, request, **kwargs):
        now = datetime.datetime.now()
        if self.form.is_valid():
            word_slug = kwargs.get("word_slug")
            tup_data = [word_slug, now.timestamp()]
            if word_slug in self.list_slugs:
                el_index = self.list_slugs.index(word_slug)
                request.session['repeat_words'].pop(el_index)
            else:
                request.session['repeat_words'].append(tup_data)
            self.list_slugs = self.get_session_data
            return redirect(reverse(
                viewname=f"{self.res.namespace}:{self.get_url_name}", kwargs=self.get_url_kwargs
            ))


class RepetitionNavigatingPagesMixin(RepetitionWordsMixin, BaseDetailView):
    """- Пагинация в повторе"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous"] = self.get_previous_page
        context["next"] = self.get_next_page
        context["all_count"] = len(self.list_slugs)  # количество всех данных в массиве сессии
        # число, номер текущего индекса в массиве сессии
        context["last_count"] = sum([int(len(self.list_slugs[:self.get_index_page])), 1])
        return context

    @property
    def get_index_page(self):
        """- Получить индекс страницу"""
        word_slug = self.kwargs.get("word_slug")
        if word_slug:
            return self.list_slugs.index(word_slug)

    def get_url_page(self, page_slug):
        """- Получить ссылку на страницу"""
        res = resolve(self.request.path)
        res.kwargs["word_slug"] = self.list_slugs[page_slug]
        return reverse(viewname=res.view_name, kwargs=res.kwargs)

    @property
    def get_previous_page(self):
        """- Получить предыдущею страницу"""
        ind = self.get_index_page - 1
        if ind < 0:
            return None
        return self.get_url_page(ind)

    @property
    def get_next_page(self):
        """- Получить следующею страницу"""
        ind = self.get_index_page + 1
        if ind >= len(self.list_slugs):
            return None
        return self.get_url_page(ind)
