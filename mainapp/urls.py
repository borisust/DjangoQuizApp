from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/register', views.registration, name='registration'),
    path('users/login', views.authentication, name='authentication'),
    path('users/logoff', views.logoff, name='logoff'),
    path('users/me', views.userProfile, name='userProfile'),
    path('quizzes/create', views.createQuiz, name='createQuiz'),
    path('quizzes/<int:quizID>', views.editQuiz, name='editQuiz'),
    path('quizzes/<int:quizID>/add_question', views.addQuestion, name='addQuestion'),
    path('quizzes/<int:quizID>/delete', views.deleteQuiz, name='deleteQuiz'),
    path('questions/<int:questionID>/delete', views.deleteQuestion, name='deleteQuestion'),
    path('questions/<int:questionID>', views.editQuestion, name='editQuestion')
]
