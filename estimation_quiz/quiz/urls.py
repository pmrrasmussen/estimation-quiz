from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    path("", views.home, name="home"),
    path("standings/", views.standings, name="standings"),
    path("questions/", views.questions, name="questions"),
    path("rules/", views.rules, name="rules"),
    path("login/", views.login_page, name="login"),
    path("login/attempt_login/", views.attempt_login, name="attempt_login"),
    path("logout/", views.attempt_logout, name="logout"),
    path("questions/answer/", views.answer, name="answer"),
    path("standings/reset/", views.reset_results, name="reset_results"),
]
