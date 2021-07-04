from django import template

register = template.Library()


@register.inclusion_tag("snippets/_menu.html")
def horizontal_menu(link):
    """- горизонтальное меню"""
    pass
    # print(request.get_full_path())
    # print(request.build_absolute_uri())
    # print(request.get_full_path_info())
    # print(request.path)
    #
    # print(request.resolver_match.url_name)
    # print(request.resolver_match.namespace)
    # print(request.resolver_match.app_name)

