from django.http import HttpResponse
from django.shortcuts import render


def words(request):
    """Все слова
    :param request:
    :return:
    """
    return render(request, "translator/words.html")


def card(request):
    """Карточка слова
    :param request:
    :return:
    """
    return render(request, "translator/card.html")

