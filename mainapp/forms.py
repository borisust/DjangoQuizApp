from django.forms import ModelForm

from mainapp.models import Quiz, Question


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['type', 'text', 'image', 'explanation']
        help_texts = {'explanation': 'Explanation text is shown after a quiz response is submitted.'}
