from django import template
from django.http import HttpRequest
from django.urls import reverse, resolve


register = template.Library()
http_request = HttpRequest()


@register.simple_tag
def url_next_previous():
    """concatenate all args"""
    view_name = f"url_translator:"
    print(http_request.path)

    # return reverse("url_translator:card", kwargs={"category_slug": self.category.slug, "word_slug": self.slug})
    # return 'ok'


# @register.inclusion_tag("snippets/_menu.html")
# def horizontal_menu(link):
#     """- горизонтальное меню"""
#     pass
    # print(request.get_full_path())
    # print(request.build_absolute_uri())
    # print(request.get_full_path_info())
    # print(request.path)
    #
    # print(request.resolver_match.url_name)
    # print(request.resolver_match.namespace)
    # print(request.resolver_match.app_name)

