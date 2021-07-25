from django.urls import reverse, resolve
from django.views import View

from . import models


class WordMixin(View):
    """- Переопределяет контекст"""
    allow_empty = False

    def setup(self, request, *args, **kwargs):
        """Инициализируйте атрибуты, общие для всех методов представления."""
        self.args = args
        self.kwargs = kwargs
        self.request = request
        self.model = models.Word
        # print(self.get_absolute_url("word"))
        # print(self.request.path)
        print(self.request.resolver_match)
        # print(reverse(self.request.resolver_match.view_name, kwargs=self.request.resolver_match.kwargs))

    def get_context_data(self, **kwargs):
        kwargs["previous"] = self.get_url_page("pk__lt")
        kwargs["next"] = self.get_url_page("pk__gt")
        kwargs["get_url_translate"] = self.get_url_translate()
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
        res = self.request.resolver_match
        if res.kwargs.get("word_slug"):
            res.kwargs["word_slug"] = query.slug
        return reverse(viewname=res.view_name, kwargs=res.kwargs)

    def get_url_translate(self):
        """- Ссылка для кнопки перевода контента"""
        res = resolve(self.request.path)
        if "rus" not in res.namespace:
            namespace = "rus"
        else:
            namespace = "over"
        return reverse(viewname=f"{namespace}:{res.url_name}", kwargs=res.kwargs)

    def get_absolute_url(self, url_name):
        res = resolve(self.request.path)
        return reverse(viewname=f"{res.namespace}:{url_name}", kwargs=res.kwargs)
