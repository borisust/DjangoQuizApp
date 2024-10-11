from django.contrib import admin

from mainapp.models import Quiz, Question, AnswerOption

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(AnswerOption)
