from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    path("", views.home, name='home'),
    path("standings/", views.standings, name='standings'),
    path("questions/", views.questions, name='questions'),
    path("rules/", views.rules, name='rules'),
]
