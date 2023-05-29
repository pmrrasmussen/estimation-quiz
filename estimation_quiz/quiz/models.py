from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer = models.IntegerField()
    is_active = models.BooleanField()


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_high = models.IntegerField()
    answer_low = models.IntegerField()
    answer_date = models.DateTimeField(auto_now=True)


class Result(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_ratio = models.IntegerField(default=1)
    correct_answer = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'user'],
                name='unique_result'),
        ]
