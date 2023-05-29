from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from collections import namedtuple

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import (Question, Result,
                     get_active_questions, validate_answer,
                     create_answer_from_input, commit_answer_to_results)

from django.core.management import call_command


# Scoring and standings

def standings(request):
    contestants = User.objects.filter(groups__name="Team")
    questions = get_active_questions()

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


# Account access

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


# Rules and home

def home(request):
    return HttpResponseRedirect(reverse("quiz:rules"))


def rules(request):
    return render(request, "rules.html")


# Answering questions

def questions(request):
    questions = get_active_questions().order_by("id")

    return render(
        request,
        "questions.html",
        {
            "questions": questions,
        },
    )


def answer(request):
    question_id = request.POST["question_id"]
    lower_bound = request.POST["lower_bound"]
    upper_bound = request.POST["upper_bound"]
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    answer_valid, error_message = validate_answer(lower_bound, upper_bound)

    if answer_valid:
        answer = create_answer_from_input(
            question,
            user,
            lower_bound,
            upper_bound
        )
        commit_answer_to_results(answer)

        messages.success(request, "Answer successfully submitted")
    else:
        messages.error(request, f"Invalid input: {error_message}")

    return HttpResponseRedirect(reverse("quiz:questions"))


# Admin commands

def reset_results(request):
    call_command('reset_results')
    return HttpResponseRedirect(reverse("quiz:standings"))
