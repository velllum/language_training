from django.urls import path

from . import views

urlpatterns = [
    path('', views.words, name='words'),
    path('card', views.card, name='card'),
]
