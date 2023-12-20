from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer = models.IntegerField()
    is_active = models.BooleanField()

    def __str__(self) -> str:
        return self.question_text


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_high = models.IntegerField()
    answer_low = models.IntegerField()
    answer_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.question.question_text}: {self.answer_low} - {self.answer_high}"


class Result(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_ratio = models.IntegerField(default=1)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.question.question_text}: {self.answer_ratio}: {self.correct_answer}"


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'user'],
                name='unique_result'),
        ]


def create_answer_from_input(question, user, lower_bound, upper_bound) -> UserAnswer:
    lower_bound = int(lower_bound)
    upper_bound = int(upper_bound)

    answer = UserAnswer(
        question=question,
        user=user,
        answer_high=upper_bound,
        answer_low=lower_bound,
    )
    answer.save()

    return answer


def commit_answer_to_results(answer: UserAnswer):
    result, _ = Result.objects.get_or_create(
        user=answer.user,
        question=answer.question,
    )

    result.answer_ratio = int(answer.answer_high/answer.answer_low)
    result.correct_answer = (
        answer.answer_low <= answer.question.answer and
        answer.question.answer <= answer.answer_high
    )

    result.save()


def validate_answer(lower_bound, upper_bound):
    """
    Checks that an answer is valid and returns (answer_is_valid, error_message).
    The error message is empty if and only if the answer was valid.
    """
    try:
        lower_bound = int(lower_bound)
        upper_bound = int(upper_bound)
    except ValueError:
        return (False, "Could not convert answers to integers")

    if lower_bound < 1:
        return (False, "Lower bound <1")

    if lower_bound >= upper_bound:
        return (False, "Lower bound should be smaller than upper bound")

    return (True, "")


def get_active_questions():
    return Question.objects.filter(is_active=True)

def get_latest_answer(user, question) -> UserAnswer | None:
    question_answers = UserAnswer.objects\
        .filter(user=user)\
        .filter(question=question)\
        .order_by('-answer_date')
    if len(question_answers) > 0:
        return question_answers[0]
    return None

def get_result(user, question):
    result, _ = Result.objects.get_or_create(
            user=user,
            question=question)
    return result
