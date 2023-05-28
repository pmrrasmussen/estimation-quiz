from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Question, Result


def standings(request):
    contestants = User.objects.all()
    questions = Question.objects.order_by('id').all()

    return render(
        request,
        'standings.html',
        {
            'contestants': contestants,
            'questions': questions,
        },
    )


def login(request):
    pass


def home(request):
    return HttpResponseRedirect(reverse('quiz:rules'))


def questions(request):
    questions = Question.objects.order_by('id').all()

    return render(
        request,
        'questions.html',
        {
            'questions': questions,
        },
    )


def rules(request):
    return render(request, 'rules.html')


def answer(request, question_id, answer_high: int, answer_low: int):
    pass

