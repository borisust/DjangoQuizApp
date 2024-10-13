from django import forms

from mainapp.models import Quiz, Question, LiveQuiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['type', 'text', 'image', 'explanation']
        help_texts = {'explanation': 'Explanation text is shown after a quiz response is submitted.'}


class QuizPublishingForm(forms.ModelForm):
    class Meta:
        model = LiveQuiz
        fields = ['access', 'password']
        widgets = {
            'access': forms.RadioSelect(),
            'password': forms.PasswordInput()
        }
