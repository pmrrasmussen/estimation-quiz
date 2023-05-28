from django.contrib import admin

from .models import Question, UserAnswer, Result

admin.site.register(Question)
admin.site.register(UserAnswer)
admin.site.register(Result)
