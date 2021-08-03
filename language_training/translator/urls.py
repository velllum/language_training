from django.urls import path, include

from . import views


word_patterns = ([
    path('', views.Word.as_view(), name='word'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.Register.as_view(), name='register'),
    path('settings/', views.settings, name='settings'),
    path('repeat-words/', views.repeat_words, name='repeat_words'),
    path('search/', views.search, name='search'),
    path('audio-replay/', views.AudioReplay.as_view(), name='audio_replay'),
    path('<word_slug>/', views.ShowWord.as_view(), name='card'),
    path('repeat-words/extend-replay', views.ExtendReplay.as_view(), name='extend_replay'),
], "url_translator")


urlpatterns = [
    path('gtts/', views.gtts, name='gtts'),
    path('', views.Category.as_view(), name='category'),
    path('russian-<category_slug>/', include(word_patterns, namespace="rus")),
    path('<category_slug>-russian/', include(word_patterns, namespace="over")),
]


