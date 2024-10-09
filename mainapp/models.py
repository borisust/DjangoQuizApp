from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Quiz(models.Model):
    is_graded = models.BooleanField(default=True)
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class AbstractQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/', default=None, blank=True, null=True)
    explanation = models.CharField(max_length=150, default=None, blank=True, null=True)

    class Meta:
        abstract = True


class MultiChoiceQuestion(AbstractQuestion):
    is_single_answer = models.BooleanField(default=True)


class MultiChoiceAnswerOption(models.Model):
    question = models.ForeignKey(MultiChoiceQuestion, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    is_correct = models.BooleanField(default=False)


class NumericQuestion(AbstractQuestion):
    correct_answer = models.FloatField()
    error_margin = models.FloatField()


class TextQuestion(AbstractQuestion):
    is_case_sensitive = models.BooleanField(default=True)
    max_characters = models.IntegerField()


class TextAnswerOption(models.Model):
    question = models.ForeignKey(TextQuestion, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)


class QuizResponse(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class MultiChoiceQuestionResponse(models.Model):
    response = models.ForeignKey(QuizResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(MultiChoiceQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(MultiChoiceAnswerOption, on_delete=models.CASCADE)


class NumericQuestionResponse(models.Model):
    response = models.ForeignKey(QuizResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(NumericQuestion, on_delete=models.CASCADE)
    answer = models.FloatField()


class TextQuestionResponse(models.Model):
    response = models.ForeignKey(QuizResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(TextQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=150)
