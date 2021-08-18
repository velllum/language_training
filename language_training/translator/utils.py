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
    """- Ссылка перевода контента"""

    def __init__(self):
        super().__init__()
        self.object = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form = forms.RepetitionWordsForm(request.POST or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_hidden"] = self.form
        context["form_hidden"].fields['id'].initial = self.object.pk
        return context

    def post(self, request, **kwargs):
        form = forms.RepetitionWordsForm(request.POST or None)
        res = resolve(request.path)
        if form.is_valid():
            idd = form.cleaned_data.get("id")
            print("form", idd)
            # user = User.objects.get(email=email)
            return redirect(reverse(f"{res.namespace}:word", kwargs={"category_slug": kwargs.get("category_slug")}))


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


