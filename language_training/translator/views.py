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
    paginator = Paginator(words, 10)
    page_number = request.GET.get('page')
    page_words = paginator.get_page(page_number)
    content = {
        "page_words": page_words,
        "category_slug": category_slug,
    }
    return render(request, "translator/words.html", context=content)


def card(request, word_slug, category_slug):
    """- Карточка слова"""
    card_word = get_object_or_404(models.Word, slug=word_slug)
    return render(request, "translator/card.html", context={"card_word": card_word, "category_slug": category_slug})


def audio_replay(request, category_slug):
    """- Аудио повтор слов добавленных в закладки"""
    print(category_slug)
    return render(request, "translator/audio_replay.html", context={"category_slug": category_slug})


def repeat_words(request, category_slug):
    """- Повторение слов добавленных в закладки"""
    return render(request, "translator/repeat_words.html", context={"category_slug": category_slug})


def extend_replay(request, category_slug):
    """- Продление повтора"""
    return render(request, "translator/extend_replay.html", context={"category_slug": category_slug})


def settings(request, category_slug):
    """- Настойки"""
    return render(request, "translator/settings.html", context={"category_slug": category_slug})


def auth(request, category_slug):
    """- Авторизация"""
    return render(request, "translator/auth.html", context={"category_slug": category_slug})


def register(request, category_slug):
    """- Регистрация"""
    return render(request, "translator/register.html", context={"category_slug": category_slug})

