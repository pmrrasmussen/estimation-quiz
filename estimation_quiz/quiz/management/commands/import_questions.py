from quiz.models import Question

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("qset", nargs=1, type=str)
        parser.add_argument(
            "--delete-old-questions",
            action="store_true",
            help="Deletes the already existing questions form the database",
        )
        parser.add_argument(
            "--deactivate-old-questions",
            action="store_true",
            help="Deletes the already existing questions form the database",
        )
        parser.add_argument(
            "--silent",
            action="store_true",
            help="Stops output at the end",
        )

    def handle(self, *args, **options):
        if options['delete_old_questions']:
            Question.objects.all().delete()

        if options['deactivate_old_questions']:
            for question in Question.objects.all():
                question.is_active = False
                question.save()

        try:
            question_set = options['qset'][0]
            questions_file_name = f"{question_set}.csv"
        except Exception:
            raise CommandError("No question set specified.")

        questions_file_path = f"quiz/questions/{questions_file_name}"

        questions = []

        with open(questions_file_path) as questions_file:
            for line in questions_file.readlines():
                try:
                    question_text, answer = line.split(";")
                    answer = int(answer)
                except ValueError:
                    raise CommandError(f"Aborting. Ill-formated line: {line}")

                questions.append(Question(
                    question_text=question_text,
                    answer=answer,
                    is_active=True,
                ))

        for question in questions:
            question.save()
            if not options['silent']:
                print(f"Stored question: {question.question_text}")
