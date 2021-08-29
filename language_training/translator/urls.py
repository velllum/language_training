from django.urls import path, include

from . import views


word_patterns = ([
    path('', views.Word.as_view(), name='word'),
    path('auth/', views.Login.as_view(), name='auth'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('settings/', views.settings, name='settings'),
    path('search/', views.search, name='search'),
    path('<word_slug>/', views.ShowWord.as_view(), name='card'),
    path('audio-replay/<word_slug>/', views.AudioReplay.as_view(), name='audio_replay'),
    path('repeat-words/<word_slug>/', views.RepeatWords.as_view(), name='repeat_words'),
    path('repeat-words/extend-replay/<word_slug>/', views.ExtendReplay.as_view(), name='extend_replay'),
], "url_translator")


urlpatterns = [
    path('', views.Category.as_view(), name='category'),
    path('russian-<category_slug>/', include(word_patterns, namespace="rus")),
    path('<category_slug>-russian/', include(word_patterns, namespace="over")),
]


