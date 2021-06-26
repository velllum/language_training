from django.http import HttpResponse
from django.shortcuts import render


def category(request):
    """Все категории
    :param request:
    :return:
    """
    return render(request, "translator/categories.html")


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


def audio_replay(request):
    """Аудио повтор слов добавленных в закладки
    :param request:
    :return:
    """
    return render(request, "translator/audio_replay.html")


def repeat_words(request):
    """Повторение слов добавленных в закладки
    :param request:
    :return:
    """
    return render(request, "translator/repeat_words.html")


def extend_replay(request):
    """Продление повтора
    :param request:
    :return:
    """
    return render(request, "translator/extend_replay.html")

