from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.category, name='category'),
    path('auth/', views.auth, name='auth'),
    path('settings/', views.settings, name='settings'),
    path('audio-replay/', views.audio_replay, name='audio_replay'),
    path('repeat-words/', views.repeat_words, name='repeat_words'),
    path('extend-replay/', views.extend_replay, name='extend_replay'),

    path('<str:category_slug>/', include([
        path('', views.word, name='word'),
        path('<str:word_slug>/', views.card, name='card'),
    ])),
]

