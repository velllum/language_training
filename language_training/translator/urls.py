from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Category.as_view(), name='category'),
    path('<category_slug>/', include([
        path('', views.word, name='word'),
        path('auth/', views.auth, name='auth'),
        path('register/', views.register, name='register'),
        path('settings/', views.settings, name='settings'),
        path('audio-replay/', views.audio_replay, name='audio_replay'),
        path('repeat-words/', views.repeat_words, name='repeat_words'),
        path('<word_slug>/', views.card, name='card'),
        path('repeat-words/extend-replay', views.extend_replay, name='extend_replay'),
    ])),
]



