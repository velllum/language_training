from django.urls import resolve, reverse
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
        res = resolve(self.request.path)
        print(res)
        print(reverse(res.view_name, kwargs=res.kwargs))

    def get_context_data(self, **kwargs):
        kwargs["previous"] = self.get_url_page("pk__lt")
        kwargs["next"] = self.get_url_page("pk__gt")
        kwargs["get_url_translate"] = self.get_url()
        return kwargs

    def get_url_page(self, pk__):
        """- Получить ссылку следующей и новой статьи"""
        res = resolve(self.request.path)
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
        if res.kwargs.get("word_slug"):
            res.kwargs["word_slug"] = query.slug
        return reverse(res.view_name, kwargs=res.kwargs)

    def get_url(self):
        """- Ссылка для кнопки перевода контента"""
        res = resolve(self.request.path)
        if "rus" not in res.namespace:
            view_name = f"rus:{res.url_name}"
        else:
            view_name = f"over:{res.url_name}"
        return reverse(viewname=view_name, kwargs=res.kwargs)

    def get_menu_url(self):
        res = resolve(self.request.path)
        if "rus" not in res.namespace:
            view_name = f"rus:{res.url_name}"
        else:
            view_name = f"over:{res.url_name}"
        return reverse(viewname=view_name, kwargs=res.kwargs)
