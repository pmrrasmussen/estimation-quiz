from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from collections import namedtuple

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Question, UserAnswer, Result


def standings(request):
    contestants = User.objects.filter(groups__name="Team")
    questions = Question.objects.order_by("id").all()

    Outcome = namedtuple('Outcome', ['contestant', 'scores', 'total'])

    outcomes = []

    for contestant in contestants:
        contestant_scores = get_contestant_scores(contestant, questions)
        contestant_total = get_total_from_scores(contestant_scores)

        outcomes.append(
            Outcome(contestant.username, contestant_scores, contestant_total)
        )

    return render(
        request,
        "standings.html",
        {
            "outcomes": outcomes,
            "questions": questions,
        },
    )


def get_contestant_scores(contestant, questions):
    contestant_scores = []
    for question in questions:
        result, _ = Result.objects.get_or_create(
            user=contestant,
            question=question)
        contestant_scores.append(
            result.answer_ratio if result.correct_answer else '-'
        )
    return contestant_scores


def get_total_from_scores(scores):
    additive_part = 10+sum([score for score in scores if score != '-'])
    multiplicative_part = 2**scores.count('-')

    return additive_part*multiplicative_part


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

    if answer_is_valid(request, lower_bound, upper_bound):
        process_answer(question, user, lower_bound, upper_bound)
        messages.success(request, "Answer successfully submitted")

    return HttpResponseRedirect(reverse("quiz:questions"))


def process_answer(question, user, lower_bound, upper_bound):
    lower_bound = int(lower_bound)
    upper_bound = int(upper_bound)

    answer = UserAnswer(
        question=question,
        user=user,
        answer_high=upper_bound,
        answer_low=lower_bound,
    ).save()

    result, _ = Result.objects.get_or_create(user=user, question=question)

    result.answer_ratio = int(upper_bound/lower_bound)
    result.correct_answer = lower_bound <= question.answer <= upper_bound

    result.save()


def answer_is_valid(request, lower_bound, upper_bound):
    try:
        lower_bound = int(lower_bound)
        upper_bound = int(upper_bound)
    except ValueError:
        messages.error(request, "Invalid input: Could not convert input to integers.")
        return False

    if lower_bound < 1:
        messages.error(request, "Invalid input: Lower bound <1.")
        return False

    if lower_bound >= upper_bound:
        messages.error(request, "Invalid input: Lower bound should be smaller than upper bound.")
        return False

    return True

