from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from . import models


def category(request):
    """- Все категории"""
    categories = models.Category.objects.all()
    return render(request, "translator/category.html", context={'categories': categories})


def word(request, category_slug):
    """- Все слова"""
    words = models.Word.objects.filter(category__slug=category_slug)
    paginator = Paginator(words, 5)
    page_number = request.GET.get('page')
    page_words = paginator.get_page(page_number)
    content = {
        "page_words": page_words,
        "category_slug": category_slug,
    }
    return render(request, "translator/words.html", context=content)


def card(request, word_slug, *args, **kwargs):
    """- Карточка слова"""
    card_word = get_object_or_404(models.Word, slug=word_slug)
    return render(request, "translator/card.html", context={"card_word": card_word})


def audio_replay(request):
    """- Аудио повтор слов добавленных в закладки"""
    return render(request, "translator/audio_replay.html")


def repeat_words(request):
    """- Повторение слов добавленных в закладки"""
    return render(request, "translator/repeat_words.html")


def extend_replay(request):
    """- Продление повтора"""
    return render(request, "translator/extend_replay.html")


def settings(request):
    """- Настойки"""
    return render(request, "translator/settings.html")


def auth(request):
    """- Авторизация"""
    return render(request, "translator/auth.html")

