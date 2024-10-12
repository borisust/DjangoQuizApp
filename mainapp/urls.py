from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/register', views.registration, name='registration'),
    path('users/login', views.authentication, name='authentication'),
    path('quizzes/create', views.createQuiz, name='createQuiz'),
    path('quizzes/<int:quizID>', views.editQuiz, name='editQuiz'),
    path('quizzes/<int:quizID>/add_question', views.addQuestion, name='addQuestion'),
    path('questions/<int:questionID>/delete', views.deleteQuestion, name='deleteQuestion'),
    path('questions/<int:questionID>', views.editQuestion, name='editQuestion')
]
