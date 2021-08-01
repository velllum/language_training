
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


