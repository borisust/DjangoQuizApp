import os.path

from django.http import QueryDict, JsonResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.templatetags.static import static
from django.urls import reverse

from mainapp.forms import QuizForm, QuestionForm, QuizPublishingForm
from mainapp.models import Quiz, AnswerOption, Question, LiveQuiz, QuizResponse, QuestionResponse


# Create your views here.


def home(request):
    return render(request, 'home.html')


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {'form': form})


def authentication(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logoff(request):
    logout(request)
    return redirect('home')


def createQuiz(request):
    if request.user.is_authenticated:
        quiz = Quiz(author=request.user)
        quiz.save()
        return redirect('editQuiz', quizID=quiz.pk)
    return redirect('authentication')


def editQuiz(request, quizID):
    try:
        quiz = Quiz.objects.get(pk=quizID)
    except Quiz.DoesNotExist:
        raise Http404
    if request.user != quiz.author:
        return redirect('home')
    if quiz.live:
        return redirect('userProfile')
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quizForm = QuizForm(request.POST, instance=quiz)
        if quizForm.is_valid():
            quizForm.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': quizForm.errors})
    quizForm = QuizForm(instance=quiz)
    questionForm = QuestionForm()
    publishForm = QuizPublishingForm()
    questions = Question.objects.filter(quiz=quiz)
    context = {'id': quizID, 'quizForm': quizForm, 'questionForm': questionForm, 'publishForm': publishForm, 'questions': questions}
    return render(request, 'quizzes/creator.html', context)


def addQuestion(request, quizID):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        # ajax only
        return redirect('editQuiz', quizID=quizID)
    try:
        quiz = Quiz.objects.get(pk=quizID)
    except Quiz.DoesNotExist:
        raise Http404
    if request.user != quiz.author or request.method != 'POST' or quiz.live:
        return HttpResponseForbidden(request)
    form = QuestionForm(request.POST, request.FILES)
    if form.is_valid():
        question = form.save(commit=False)
        question.quiz = quiz
        answerCount = int(request.POST['answer_count'])
        if answerCount < 2:
            errors = {'answer_count': 'At least 2 answer options are required.'}
            return JsonResponse({'success': False, 'errors': errors})
        answersList = []
        correctAnswers = request.POST.getlist('correct_answers')
        for i in range(1, answerCount+1):
            if ('answer_'+str(i)+'_text') not in request.POST or request.POST['answer_'+str(i)+'_text'] == "":
                errors = {'answer_count': 'Answer text cannot be blank.'}
                return JsonResponse({'success': False, 'errors': errors})
            answerText = request.POST['answer_'+str(i)+'_text']
            answerIsCorrect = str(i) in correctAnswers
            answer = AnswerOption(text=answerText, is_correct=answerIsCorrect, question=question)
            answersList.append(answer)
        question.save()
        for answer in answersList:
            answer.save()
        if question.image:
            url = question.image.url
        else:
            url = static('placeholder.svg')
        return JsonResponse({'success': True, 'id': question.id, 'text': question.text, 'image': url})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})


def deleteQuestion(request, questionID):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        # ajax only
        return redirect('home')
    try:
        question = Question.objects.get(pk=questionID)
    except Question.DoesNotExist:
        raise Http404
    if request.user != question.quiz.author or request.method != 'POST' or question.quiz.live:
        return HttpResponseForbidden(request)
    question.delete()
    return JsonResponse({'success': True})


def editQuestion(request, questionID):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        # ajax only
        return redirect('home')
    try:
        question = Question.objects.get(pk=questionID)
    except Question.DoesNotExist:
        raise Http404
    if request.user != question.quiz.author or question.quiz.live:
        return HttpResponseForbidden(request)
    if request.method == 'GET':
        form = QuestionForm(instance=question)
        answers = AnswerOption.objects.filter(question=question)
        return render(request, 'quizzes/_question_editor.html', {'question': question, 'form': form, 'answers': answers})
    form = QuestionForm(request.POST, request.FILES, instance=question)
    if form.is_valid():
        answerCount = int(request.POST['answer_count'])
        if answerCount < 2:
            errors = {'answer_count': 'At least 2 answer options are required.'}
            return JsonResponse({'success': False, 'errors': errors})
        answersList = []
        correctAnswers = request.POST.getlist('correct_answers')
        for i in range(1, answerCount+1):
            if ('answer_'+str(i)+'_text') not in request.POST or request.POST['answer_'+str(i)+'_text'] == "":
                errors = {'answer_count': 'Answer text cannot be blank.'}
                return JsonResponse({'success': False, 'errors': errors})
            answerText = request.POST['answer_'+str(i)+'_text']
            answerIsCorrect = str(i) in correctAnswers
            answer = AnswerOption(text=answerText, is_correct=answerIsCorrect, question=question)
            answersList.append(answer)
        form.save()
        oldAnswers = AnswerOption.objects.filter(question=question)
        for answer in oldAnswers:
            answer.delete()
        for answer in answersList:
            answer.save()
        if question.image:
            url = question.image.url
        else:
            url = static('placeholder.svg')
        return JsonResponse({'success': True, 'edit': True, 'id': question.id, 'text': question.text, 'image': url})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})


def userProfile(request):
    if request.user.is_authenticated:
        savedQuizzes = Quiz.objects.filter(author=request.user, live=None).order_by('-created_at')
        liveQuizzes = LiveQuiz.objects.filter(quiz__author=request.user).order_by('-published_at')
        responses = QuizResponse.objects.filter(responder=request.user).order_by('-submitted_at')
        context = {'quizzes': savedQuizzes, 'liveQuizzes': liveQuizzes,'responses': responses, 'username': request.user.username}
        return render(request, 'users/profile.html', context)
    return redirect('authentication')


def deleteQuiz(request, quizID):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        # ajax only
        return redirect('home')
    try:
        quiz = Quiz.objects.get(pk=quizID)
    except Quiz.DoesNotExist:
        raise Http404
    if request.user != quiz.author or request.method != 'POST' or quiz.live:
        return HttpResponseForbidden(request)
    quiz.delete()
    return JsonResponse({'success': True})


def publishQuiz(request, quizID):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        # ajax only
        return redirect('home')
    try:
        quiz = Quiz.objects.get(pk=quizID)
    except Quiz.DoesNotExist:
        raise Http404
    if request.user != quiz.author or request.method != 'POST' or quiz.live:
        return HttpResponseForbidden(request)
    questions = Question.objects.filter(quiz=quiz).count()
    if questions < 1:
        return JsonResponse({'success': False, 'msg': 'You must add at least one question before publishing.'})
    form = QuizPublishingForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False, 'msg': 'Invalid quiz access.'})
    liveQuiz = form.save(commit=False)
    liveQuiz.quiz = quiz
    liveQuiz.save()
    quiz.live = liveQuiz
    quiz.save()
    return JsonResponse({'success': True, 'url': reverse('userProfile')})


def quizzes(request):
    publicQuizzes = LiveQuiz.objects.filter(access='PUB').order_by('-published_at')
    return render(request, 'quizzes/quizzes.html', {'quizzes': publicQuizzes})


def viewQuiz(request, liveID):
    try:
        liveQuiz = LiveQuiz.objects.get(pk=liveID)
    except LiveQuiz.DoesNotExist:
        raise Http404
    if liveQuiz.access == 'PRT' and not (request.method == 'POST' and request.POST.get('password') == liveQuiz.password):
        context = {'url': reverse('viewQuiz', kwargs={'liveID': liveID}), 'failed': request.method == 'POST'}
        return render(request, 'password.html', context)
    if liveQuiz.access == 'PRV' and request.user != liveQuiz.quiz.author:
        return HttpResponseForbidden(request)
    questions = Question.objects.filter(quiz=liveQuiz.quiz)
    return render(request, 'quizzes/quiz.html', {'liveQuiz': liveQuiz, 'questions': questions})


def manageLiveQuiz(request, liveID):
    try:
        liveQuiz = LiveQuiz.objects.get(pk=liveID)
    except LiveQuiz.DoesNotExist:
        raise Http404
    if request.user != liveQuiz.quiz.author:
        return HttpResponseForbidden(request)
    if request.method == 'POST':
        form = QuizPublishingForm(request.POST, instance=liveQuiz)
        if form.is_valid():
            form.save()
            return redirect('manageLive', liveID=liveID)
    else:
        form = QuizPublishingForm(instance=liveQuiz)
    return render(request, 'quizzes/manage.html', {'form': form, 'liveQuiz': liveQuiz})


def unpublishQuiz(request, liveID):
    try:
        liveQuiz = LiveQuiz.objects.get(pk=liveID)
    except LiveQuiz.DoesNotExist:
        raise Http404
    if request.user != liveQuiz.quiz.author:
        return HttpResponseForbidden(request)
    liveQuiz.delete()
    return redirect('userProfile')


def submitResponse(request, liveID):
    if request.method != 'POST':
        return redirect('viewQuiz', liveID=liveID)
    try:
        liveQuiz = LiveQuiz.objects.get(pk=liveID)
    except LiveQuiz.DoesNotExist:
        raise Http404
    if liveQuiz.access == 'PRT' and request.POST.get('password') != liveQuiz.password:
        return HttpResponseForbidden(request)
    if liveQuiz.access == 'PRV' and request.user != liveQuiz.quiz.author:
        return HttpResponseForbidden(request)
    user = None
    if request.user.is_authenticated:
        user = request.user
    response = QuizResponse(live=liveQuiz, responder=user)
    response.save()
    for question in liveQuiz.quiz.question_set.all():
        answers = request.POST.getlist('question_'+str(question.id))
        for answerID in answers:
            try:
                answer = AnswerOption.objects.get(pk=int(answerID))
            except AnswerOption.DoesNotExist:
                continue
            questionResponse = QuestionResponse(response=response, question=question, answer=answer)
            questionResponse.save()
    return redirect('viewResponse', responseID=response.pk)


def viewResponse(request, responseID):
    return render(request, 'quizzes/response.html')


def viewAllResponses(request, liveID):
    try:
        liveQuiz = LiveQuiz.objects.get(pk=liveID)
    except LiveQuiz.DoesNotExist:
        raise Http404
    if request.user != liveQuiz.quiz.author:
        return HttpResponseForbidden(request)
    responses = QuizResponse.objects.filter(live=liveQuiz)
    return render(request, 'quizzes/all_responses.html', {'responses': responses})