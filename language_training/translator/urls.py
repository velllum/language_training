from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.Category.as_view(), name='category'),
    path('<category_slug>/', views.word, name='word'),
    path('<category_slug>/auth/', views.auth, name='auth'),
    path('<category_slug>/register/', views.register, name='register'),
    path('<category_slug>/settings/', views.settings, name='settings'),
    path('<category_slug>/audio-replay/', views.audio_replay, name='audio_replay'),
    path('<category_slug>/repeat-words/', views.repeat_words, name='repeat_words'),
    path('<category_slug>/<word_slug>/', views.card, name='card'),
    path('<category_slug>/repeat-words/extend-replay', views.extend_replay, name='extend_replay'),

    # path('<str:category_slug>/', include([
    #     path('', views.word, name='word'),
    #     path('<str:word_slug>/', views.card, name='card'),
    # ])),
]



