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
        self.filter_list_slugs = None
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
        context["name_space"] = self.name_space
        return context

    def get_url_translate(self):
        """- Ссылка для кнопки перевода контента"""
        res = resolve(self.request.path)
        if "rus" not in res.namespace:
            namespace = self.rus_ns
        else:
            namespace = self.over_ns
        return reverse(viewname=f"{namespace}:{self.res.url_name}", kwargs=self.res.kwargs)


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
        if self.res.kwargs.get("word_slug"):
            self.res.kwargs["word_slug"] = query.slug
        return reverse(viewname=self.res.view_name, kwargs=self.res.kwargs)


class AddReplayWordMixin(BaseMixin, BaseDetailView):
    """- Добавить, удалить слова из повтора"""
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.list_slugs = self.get_session_list_slugs
        self.filter_list_slugs = self.get_filter_list_slugs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_list_slugs"] = self.get_filter_list_slugs
        return context

    @property
    def get_filter_list_slugs(self):
        """- получить фильтрованные данные по дате и времени"""
        list_slugs = []
        date = datetime.datetime.now().timestamp()
        for slug, time, _ in self.request.session.get("repeat_words", None):
            if time > date:
                continue
            list_slugs.append(slug)
        return list_slugs

    @property
    def get_session_list_slugs(self):
        """- получить данные из сессии,
        - если сессия пустая создать пустой список"""
        repeat_words = self.request.session.get("repeat_words", None)
        if repeat_words:
            return [slug for slug, _, _ in repeat_words]
        return self.request.session.setdefault('repeat_words', [])

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
        list_slugs = self.filter_list_slugs
        len_list = len(list_slugs) - 1
        if word_slug in list_slugs:
            ind = list_slugs.index(word_slug)
            if len_list != ind and len_list > ind:
                ind += 1
            else:
                ind -= 1
            self.next_redirect_page = list_slugs[ind]

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

    def get_current_interval(self, request, word_slug):
        """- получить присвоенный интервал дня повтора, при добавлении"""
        if word_slug in self.list_slugs:
            ind = self.list_slugs.index(word_slug)
            print("интервал дня повтора", request.session['repeat_words'][ind][2])
            return request.session['repeat_words'][ind][2]

    @staticmethod
    def update_date_repeat(day_interval, hour=1):
        """- обновить дату повтора"""
        return datetime.datetime.combine(
            date=datetime.date.today() + datetime.timedelta(days=day_interval),
            time=datetime.time(hour=hour)
        )

    def increase_current_interval(self, request, word_slug, interval):
        """- увеличить текущий интервал"""
        if word_slug in self.list_slugs and interval in self.list_repeat_day_interval:
            ind_slug = self.list_slugs.index(word_slug)
            ind_interval = self.list_repeat_day_interval.index(interval)
            len_repeat_interval = len(self.list_repeat_day_interval) - 1
            if len_repeat_interval != ind_interval and len_repeat_interval > ind_interval:
                ind_interval += 1
            new_current_interval = self.list_repeat_day_interval[ind_interval]
            request.session['repeat_words'][ind_slug] = new_current_interval
            return new_current_interval

    def post(self, request, **kwargs):
        """- события по кнопкам добавления повтора и т.д."""
        word_slug = kwargs.get("word_slug")
        now = datetime.datetime.now()  # получить текущею дату
        current_interval = self.get_current_interval(request, word_slug)  # получить текущий интервал
        self.get_next_redirect_page()  # получить данные для редиректа

        if self.btn_today in request.POST:
            """- добавить, удалить данные из сессии"""
            tup_data = [word_slug, now.timestamp(), self.list_repeat_day_interval[0]]
            self.add_to_extract_session_data(request, word_slug, tup_data)

        elif self.btn_repeat in request.POST:
            """- добавить данные в сессии, повторить еще раз сегодня (отправляется в конец)"""
            tup_data = [word_slug, now.timestamp(), current_interval]
            self.add_time_replay_session(request, word_slug, tup_data)

        elif self.btn_next_day in request.POST:
            """- продлить временную точку повтора"""
            # получить дату следующего показа (обновить дату след показа)
            new_date_repeat = self.update_date_repeat(current_interval)
            print(new_date_repeat, new_date_repeat.timestamp())
            # увеличить интервал на следующий
            new_current_interval = self.increase_current_interval(request, word_slug, current_interval)
            # добавить параметр указывающий о наличии интервала времени
            tup_data = [word_slug, new_date_repeat.timestamp(), new_current_interval]
            # удаляем и добавляем в конец списка
            self.add_time_replay_session(request, word_slug, tup_data)

        # переопределяем список list_slugs
        self.list_slugs = self.get_session_list_slugs
        # переопределяем список filter_list_slugs
        self.filter_list_slugs = self.get_filter_list_slugs

        # переадресация
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
        context["name_space"] = self.name_space
        context["all_count"] = len(self.filter_list_slugs)  # количество всех данных в массиве сессии
        # число, номер текущего индекса в массиве сессии
        context["last_count"] = sum([int(len(self.filter_list_slugs[:self.get_index_page])), 1])
        context["interval"] = self.get_current_interval(self.request, self.kwargs["word_slug"])
        return context

    @property
    def get_index_page(self):
        """- Получить индекс страницу"""
        word_slug = self.kwargs.get("word_slug")
        print(self.filter_list_slugs, len(self.filter_list_slugs))
        print(self.list_slugs, len(self.list_slugs))
        print(word_slug)
        if word_slug in self.filter_list_slugs:
            ind = self.filter_list_slugs.index(word_slug)
            return ind

    def get_url_page(self, page_ind):
        """- Получить ссылку на страницу"""
        res = resolve(self.request.path)
        res.kwargs["word_slug"] = self.filter_list_slugs[page_ind]
        return reverse(viewname=res.view_name, kwargs=res.kwargs)

    @property
    def get_previous_page(self):
        """- Получить предыдущею страницу"""
        ind = self.get_index_page
        print('ind', ind)
        # if not ind:
        #     return None
        # if ind < 0:
        #     return None
        if ind:
            return self.get_url_page(ind - 1)

    @property
    def get_next_page(self):
        """- Получить следующею страницу"""
        ind = self.get_index_page
        # if not ind:
        #     return None
        # if ind >= len(self.filter_list_slugs):
        #     return None
        if ind:
            return self.get_url_page(ind + 1)
