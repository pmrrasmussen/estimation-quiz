# Generated by Django 4.2.1 on 2023-05-29 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_useranswer_answer_date'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='result',
            constraint=models.UniqueConstraint(fields=('question', 'user'), name='unique_result'),
        ),
    ]
