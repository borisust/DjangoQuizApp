from django.db import models

# Create your models here.


class Quiz(models.Model):
    class QuizType(models.TextChoices):
        GRADED = 'GR'
        UNGRADED = 'UG'

    quizType = models.CharField(max_length=2, choices=QuizType.choices)
    quizTitle = models.CharField(max_length=50)
