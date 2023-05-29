from quiz.models import (
    UserAnswer,
    Result,
    commit_answer_to_results,
    validate_answer
    )

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.erase_results()
        self.recompute_results()

    def recompute_results(self):
        for answer in UserAnswer.objects.order_by("answer_date"):
            valid, _ = validate_answer(
                lower_bound=answer.answer_low,
                upper_bound=answer.answer_high
            )

            if valid:
                commit_answer_to_results(answer)

    def erase_results(self):
        Result.objects.all().delete()


