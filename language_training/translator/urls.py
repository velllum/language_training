from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.category, name='category'),
    path('<slug:category_slug>/', include([
        path('', views.word, name='word'),
        path('audio-replay/', views.audio_replay, name='audio_replay'),
        path('repeat-words/', views.repeat_words, name='repeat_words'),
        path('extend-replay/', views.extend_replay, name='extend_replay'),
        path('<str:word_slug>', views.card, name='card'),
    ])),
]