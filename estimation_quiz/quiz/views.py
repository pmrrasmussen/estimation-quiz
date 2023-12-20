from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from collections import namedtuple, defaultdict
from typing import NamedTuple

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import (Question, Result,
                     get_active_questions, validate_answer,
                     create_answer_from_input, commit_answer_to_results,
                     get_result, get_latest_answer)

from .templatetags.quiz_extras import remaining_guesses

from django.core.management import call_command


# Scoring and standings

def standings(request):
    contestants = User.objects.filter(is_superuser=False)
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
        result = get_result(contestant, question)
        contestant_scores.append(
            get_score_from_result(result)
        )
    return contestant_scores

def get_score_from_result(result: Result) -> str | int:
    return result.answer_ratio if result.correct_answer else '-'

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
class QuestionRow(NamedTuple):
    question: Question
    lower_bound: str = ''
    upper_bound: str = ''
    score: str = '-'

def questions(request):
    questions = get_active_questions().order_by("id")
    non_admin_users = User.objects.filter(is_superuser=False)
    question_rows = [get_question_row(request.user, question) for question in questions]

    return render(
        request,
        "questions.html",
        {
            "questions": questions,
            "contestants": non_admin_users,
            "question_rows": question_rows,
        },
    )

def get_question_row(user: User, question: Question) -> QuestionRow:
    if user.is_superuser or not user.is_authenticated:
        return QuestionRow(question=question)

    latest_answer = get_latest_answer(user, question)
    lower_bound = '' if latest_answer is None else str(latest_answer.answer_low)
    upper_bound = '' if latest_answer is None else str(latest_answer.answer_high)

    result = get_result(user, question)
    score = str(get_score_from_result(result))

    return QuestionRow(
        question=question,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        score=score
    )

def answer(request):
    question_id = request.POST["question_id"]
    lower_bound = request.POST["lower_bound"]
    upper_bound = request.POST["upper_bound"]
    question = get_object_or_404(Question, pk=question_id)

    if 'contestant' in request.POST and request.user.is_superuser:
        contestant_id = request.POST['contestant']
        user = User.objects.get(pk=contestant_id)
    else:
        user = request.user

    answer_valid, error_message = validate_answer(lower_bound, upper_bound)

    if remaining_guesses(user) <= 0:
        answer_valid = False
        error_message = f"User {user.username} is out of guesses"

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
