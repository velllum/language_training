import copy

from django.urls import resolve, reverse
from django.views.generic.detail import BaseDetailView

from . import models


class WordMixin(BaseDetailView):
    """- Переопределяет контекст"""
    allow_empty = False

    def setup(self, request, *args, **kwargs):
        """Инициализируйте атрибуты, общие для всех методов представления."""
        self.args = args
        self.request = request
        self.kwargs = kwargs
        self.model = models.Word
        self.res = resolve(self.request.path)
        # self.get_url_translate()

    def get_url_page(self, pk__):
        """- Получить ссылку следующей и новой статьи"""
        # res = copy.deepcopy(self.res)
        # print(res)
        query = self.model.objects.filter(
            **{pk__: self.object.pk}, is_free=True, category__slug=self.kwargs['category_slug'],
        )
        if not query:
            return None
        if pk__ is "pk__lt":
            query = query.order_by("-pk").first()
        else:
            query = query.first()
        if self.res.kwargs.get("word_slug"):
            self.res.kwargs["word_slug"] = query.slug
        return reverse(self.res.view_name, kwargs=self.res.kwargs)

    def get_url_translate(self):
        """- Ссылка для кнопки перевода контента"""
        if "rus" not in self.res.namespace:
            # print(reverse(self.res.view_name, kwargs=self.res.kwargs))
            # print(self.res.view_name)
            # print(self.res.url_name)
            # print(self.res.namespace)
            # print(self.res)
            #
            # print(f"rus:{self.res.url_name}")
            return reverse(f"rus:{self.res.url_name}", kwargs=self.res.kwargs)
        else:
            return reverse(f"over:{self.res.url_name}", kwargs=self.res.kwargs)
