from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=150, default='Untitled Quiz')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    live = models.ForeignKey('LiveQuiz', default=None, blank=True, null=True, related_name='+', on_delete=models.SET_NULL)


class Question(models.Model):
    TYPES = (('RB', 'Radio Buttons'), ('CB', 'Checkboxes'))
    type = models.CharField(max_length=2, choices=TYPES, default='RB')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/', default=None, blank=True, null=True)
    explanation = models.CharField(max_length=150, default=None, blank=True, null=True)

    class Meta:
        order_with_respect_to = "quiz"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    is_correct = models.BooleanField(default=False)


class LiveQuiz(models.Model):
    ACCESS_TYPES = (('PUB', 'Public'), ('PRT', 'Password-protected'), ('PRV', 'Private'))
    quiz = models.ForeignKey(Quiz, related_name='+', on_delete=models.PROTECT)
    published_at = models.DateTimeField(auto_now_add=True)
    access = models.CharField(max_length=3, choices=ACCESS_TYPES, default='PUB')
    password = models.CharField(max_length=50, default=None, blank=True, null=True)


class QuizResponse(models.Model):
    live = models.ForeignKey(LiveQuiz, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    submitted_at = models.DateTimeField(auto_now_add=True)


class QuestionResponse(models.Model):
    response = models.ForeignKey(QuizResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)


