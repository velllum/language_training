import datetime


class CategorySlugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.slug_category = None

    def __call__(self, request):
        # Код, который выполняется в каждом запросе перед вызовом представления
        response = self.get_response(request)
        # Код, который выполняется в каждом запросе после вызова представления
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """- Этот код выполняется непосредственно перед вызовом представления"""
        resolve = request.resolver_match
        if resolve.kwargs:
            self.slug_category = resolve.kwargs.get("category_slug")
        request.slug_category = self.slug_category


class SessionListSlugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Код, который выполняется в каждом запросе перед вызовом представления
        response = self.get_response(request)
        # Код, который выполняется в каждом запросе после вызова представления
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """- Этот код выполняется непосредственно перед вызовом представления"""
        date = datetime.datetime.now().timestamp()
        repeat_words = request.session.get("repeat_words", None)
        if repeat_words:
            request.session_list_slug = [
                slug for slug, time, _ in repeat_words
                if not time > date
            ]
            print('SessionListSlugMiddleware list_filter_slug', request.session_list_slug)
            print('SessionListSlugMiddleware list_slug', request.session.get("repeat_words", None))
        else:
            request.session_list_slug = []
