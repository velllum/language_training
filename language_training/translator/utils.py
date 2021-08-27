import datetime

from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from . import models
from . import forms


class BaseMixin:
    def __init__(self):
        self.model = models.Word


class RepetitionWordsMixin(BaseMixin, BaseListView):
    """- Добавить, удалить слова из повтора"""
    def __init__(self):
        super().__init__()
        self.list_slugs = None
        self.object = None
        self.form = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form = forms.RepetitionWordsForm(request.POST or None)
        self.list_slugs = self.get_session_data(request)

    @staticmethod
    def get_session_data(request):
        """- получить данные из сессии"""
        repeat_words = request.session.get("repeat_words", None)
        if repeat_words:
            return [slug for slug, _ in repeat_words]
        else:
            return request.session.setdefault('repeat_words', [])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_hidden"] = self.form
        context["list_slugs"] = self.list_slugs
        return context

    def post(self, request, **kwargs):
        res = resolve(request.path)
        now = datetime.datetime.now()
        if self.form.is_valid():
            word_slug = kwargs.get("word_slug")
            tup_data = [word_slug, now.timestamp()]
            if word_slug in self.list_slugs:
                el_index = self.list_slugs.index(word_slug)
                request.session['repeat_words'].pop(el_index)
            else:
                request.session['repeat_words'].append(tup_data)
            return redirect(reverse(viewname=res.view_name, kwargs=res.kwargs))


class TranslateContentMixin(BaseMixin, BaseListView):
    """- Ссылка перевода контента"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["get_url_translate"] = self.get_url_translate()
        return context

    def get_url_translate(self):
        """- Ссылка для кнопки перевода контента"""
        res = resolve(self.request.path)
        if "rus" not in res.namespace:
            namespace = "rus"  # Вывести в переменную "rus", "over" setting.py
        else:
            namespace = "over"
        return reverse(viewname=f"{namespace}:{res.url_name}", kwargs=res.kwargs)


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


