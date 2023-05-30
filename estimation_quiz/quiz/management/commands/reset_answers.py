from quiz.models import UserAnswer
from django.core.management import call_command

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        UserAnswer.objects.all().delete()

        call_command('reset_results')
