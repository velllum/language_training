from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Category.as_view(), name='category'),

    path('<category_slug>/', include([
        path('', views.Word.as_view(), name='word'),
        path('auth/', views.auth, name='auth'),
        path('register/', views.Register.as_view(), name='register'),
        path('settings/', views.settings, name='settings'),
        path('audio-replay/', views.audio_replay, name='audio_replay'),
        path('repeat-words/', views.repeat_words, name='repeat_words'),

        path('<word_slug>/', views.ShowWord.as_view(), name='card'),

        path('repeat-words/extend-replay', views.extend_replay, name='extend_replay'),
    ])),
]



