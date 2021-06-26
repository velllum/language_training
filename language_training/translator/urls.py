from django.urls import path

from . import views

urlpatterns = [
    path('words', views.words, name='words'),
    path('card', views.card, name='card'),
    path('audio-replay', views.audio_replay, name='audio_replay'),
    path('repeat-words', views.repeat_words, name='repeat_words'),
    path('extend-replay', views.extend_replay, name='extend_replay'),
]
