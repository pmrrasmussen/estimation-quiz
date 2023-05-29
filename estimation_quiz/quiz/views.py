from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Question, UserAnswer, Result


def standings(request):
    contestants = User.objects.filter(groups__name="Team")
    questions = Question.objects.order_by("id").all()

    return render(
        request,
        "standings.html",
        {
            "contestants": contestants,
            "questions": questions,
        },
    )


def attempt_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("quiz:login"))
    else:
        return render(
            request,
            "login.html",
            {
                "error_message": "Invalid username or password"
            }
        )


def login_page(request):
    return render(
        request,
        "login.html",
    )


def attempt_logout(request):
    logout(request)
    return render(
        request,
        "login.html"
    )


def home(request):
    return HttpResponseRedirect(reverse("quiz:rules"))


def questions(request):
    questions = Question.objects.order_by("id").all()

    return render(
        request,
        "questions.html",
        {
            "questions": questions,
        },
    )


def rules(request):
    return render(request, "rules.html")


def answer(request):
    question_id = request.POST["question_id"]
    lower_bound = request.POST["lower_bound"]
    upper_bound = request.POST["upper_bound"]
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    if not answer_is_valid(lower_bound, upper_bound):
        messages.error(request, "Invalid input")
    else:
        process_answer(question, user, lower_bound, upper_bound)
        messages.success(request, "Answer successfully submitted")

    return HttpResponseRedirect(reverse("quiz:questions"))


def process_answer(question, user, lower_bound, upper_bound):
    answer = UserAnswer(
        question=question,
        user=user,
        answer_high=upper_bound,
        answer_low=lower_bound,
    ).save()


def answer_is_valid(lower_bound, upper_bound):
    return False
