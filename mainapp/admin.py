from django.contrib import admin

from mainapp.models import Quiz, Question, AnswerOption, LiveQuiz, QuizResponse, QuestionResponse

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(LiveQuiz)
admin.site.register(QuizResponse)
admin.site.register(QuestionResponse)
