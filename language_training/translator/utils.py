import datetime

from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.views import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from . import models


class BaseMixin(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = models.Word
        self.list_repeat_day_interval = [1, 2, 4, 9, 18, 30, 60, 120, 240, 480, 960, 1920]
        self.btn_today = "today"
        self.btn_repeat = "repeat"
        self.btn_next_day = "next_day"
        self.name_space = "rus"
        self.rus_ns = "rus"
        self.over_ns = "over"
        self.next_redirect_page = None
        self.allow_empty = False
        self.object_list = None
        self.last_count = None
        self.list_slugs = None
        self.object = None
        self.res = None
        self.form = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
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


class AddReplayWordMixin(BaseMixin, BaseDetailView):
    """- Добавить, удалить слова из повтора"""
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.list_slugs = self.get_session_list_slugs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_slugs"] = self.list_slugs
        return context

    # @property
    # def get_filter_list_slugs(self):
    #     """- получить фильтрованные данные по дате и времени"""
    #     pass
    #     list_slugs = []
    #     for slug, time, _ in self.request.session.get("repeat_words", None):
    #         if time < datetime.datetime.now().timestamp():
    #             list_slugs.append(slug)
    #     return list_slugs

    @property
    def get_session_list_slugs(self):
        """- получить данные из сессии,
        - если сессия пустая создать пустой список"""
        repeat_words = self.request.session.get("repeat_words", None)
        if repeat_words:
            return [slug for slug, _, _ in repeat_words]
        return self.request.session.setdefault('repeat_words', list())

    @property
    def get_url_kwargs(self):
        """- получить словарь kwargs"""
        return self.kwargs

    @property
    def get_url_name(self):
        """- имя страницы редиректа"""
        return self.res.url_name

    def get_next_redirect_page(self):
        """- получить следующею страницу редиректа"""
        word_slug = self.res.kwargs.get("word_slug")
        len_list = len(self.list_slugs) - 1
        if word_slug in self.list_slugs:
            ind = self.list_slugs.index(word_slug)
            if len_list != ind and len_list > ind:
                ind += 1
            elif len_list < ind or len_list == ind:
                ind -= 1
            self.next_redirect_page = self.list_slugs[ind]

    def add_to_extract_session_data(self, request, word_slug, tup_data):
        """- добавить, удалить данные из сессии"""
        if word_slug in self.list_slugs:
            ind = self.list_slugs.index(word_slug)
            request.session['repeat_words'].pop(ind)
        else:
            request.session['repeat_words'].append(tup_data)

    def add_time_replay_session(self, request, word_slug, tup_data):
        """- перенести в конец повтора"""
        if word_slug in self.list_slugs:
            ind = self.list_slugs.index(word_slug)
            request.session['repeat_words'].pop(ind)
            request.session['repeat_words'].append(tup_data)

    def get_day_interval(self, request, word_slug):
        """- получить присвоенный интервал дня повтора, при добавлении"""
        if word_slug in self.list_slugs:
            ind = self.list_slugs.index(word_slug)
            return request.session['repeat_words'][ind][2]

    def update_date_repeat(self, request, word_slug, now, day_interval):
        """- обновить дату повтора"""
        ...

    def post(self, request, **kwargs):
        word_slug = kwargs.get("word_slug")
        if self.btn_today in request.POST:
            """- добавить, удалить данные из сессии"""
            now = datetime.datetime.now()
            day_interval = self.list_repeat_day_interval[0]
            tup_data = [word_slug, now.timestamp(), day_interval]  # добавить параметр указывающий о наличии интервала времени
            self.get_next_redirect_page()
            self.add_to_extract_session_data(request, word_slug, tup_data)
            self.list_slugs = self.get_session_list_slugs
            return redirect(reverse(
                viewname=f"{self.res.namespace}:{self.get_url_name}",
                kwargs=self.get_url_kwargs
            ))

        elif self.btn_repeat in request.POST:
            """- добавить данные в сессии, повторить еще раз сегодня (отправляется в конец)"""
            now = datetime.datetime.now()
            day_interval = self.get_day_interval(request, word_slug)
            tup_data = [word_slug, now.timestamp(), day_interval]  # добавить параметр указывающий о наличии интервала времени
            print(tup_data)
            self.get_next_redirect_page()
            self.add_time_replay_session(request, word_slug, tup_data)
            self.list_slugs = self.get_session_list_slugs
            return redirect(reverse(
                viewname=f"{self.res.namespace}:{self.get_url_name}",
                kwargs=self.get_url_kwargs
            ))

        elif self.btn_next_day in request.POST:
            """- продлить временную точку повтора"""
            now = datetime.datetime.now()
            day_interval = self.get_day_interval(request, word_slug)
            new_date_repeat = self.update_date_repeat(request, word_slug, now, day_interval)
            tup_data = [word_slug, new_date_repeat.timestamp(), day_interval]  # добавить параметр указывающий о наличии интервала времени
            self.get_next_redirect_page()
            self.add_time_replay_session(request, word_slug, tup_data)
            self.list_slugs = self.get_session_list_slugs
            return redirect(reverse(
                viewname=f"{self.res.namespace}:{self.get_url_name}",
                kwargs=self.get_url_kwargs
            ))


class AddReplayWordAndNavigatingMixin(AddReplayWordMixin, BaseDetailView):
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

    @property
    def get_time_replay(self):
        """- получить временную точку повтора
        и отправить ее в шаблон контекстом"""
        ...
        return

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
