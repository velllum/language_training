from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def app(request):
    return HttpResponse("Hello Piksi")


def post(request):
    return HttpResponse("Post requests")


def words(request):
    return render(request, "translator/cover.html")
