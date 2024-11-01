from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/register', views.registration, name='registration'),
    path('users/login', views.authentication, name='authentication'),
    path('users/logoff', views.logoff, name='logoff'),
    path('users/me', views.userProfile, name='userProfile'),
    path('quizzes/create', views.createQuiz, name='createQuiz'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('quizzes/live/<int:liveID>', views.viewQuiz, name='viewQuiz'),
    path('quizzes/live/<int:liveID>/submit', views.submitResponse, name='submitResponse'),
    path('quizzes/live/<int:liveID>/manage', views.manageLiveQuiz, name='manageLive'),
    path('quizzes/live/<int:liveID>/delete', views.unpublishQuiz, name='unpublishQuiz'),
    path('quizzes/live/<int:liveID>/responses', views.viewAllResponses, name='viewAllResponses'),
    path('quizzes/<int:quizID>', views.editQuiz, name='editQuiz'),
    path('quizzes/<int:quizID>/publish', views.publishQuiz, name='publishQuiz'),
    path('quizzes/<int:quizID>/add_question', views.addQuestion, name='addQuestion'),
    path('quizzes/<int:quizID>/set_order', views.setQuestionOrder, name='setQuestionOrder'),
    path('quizzes/<int:quizID>/delete', views.deleteQuiz, name='deleteQuiz'),
    path('questions/<int:questionID>/delete', views.deleteQuestion, name='deleteQuestion'),
    path('questions/<int:questionID>', views.editQuestion, name='editQuestion'),
    path('responses/<int:responseID>', views.viewResponse, name='viewResponse')
]
