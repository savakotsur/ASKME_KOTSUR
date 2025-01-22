from django.shortcuts import render, get_object_or_404, redirect
from .utils import paginate  
from .models import Question, Tag, Answer
from django.conf.urls import handler404
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.urls import reverse
from .forms import CustomLoginForm, CustomSignupForm, ProfileEditForm, QuestionForm, AnswerForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')  
            else:
                form.add_error('password', 'Invalid username or password.')
                form.add_error('username', 'Invalid username or password.')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save() 
            auth_login(request, user)  
            return redirect('index')  
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def settings(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProfileEditForm(instance=user_profile)

    return render(request, 'settings.html', {'form': form})

def get_paginated_questions(request, queryset, template_name, extra_context=None):
    per_page = 10
    page_obj = paginate(queryset, request, per_page)
    context = {'page_obj': page_obj}
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context)

def index(request):
    questions = Question.objects.new()
    return get_paginated_questions(request, questions, 'index.html')

def hot(request):
    questions = Question.objects.popular()
    return get_paginated_questions(request, questions, 'hot.html')

def tag_questions(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.questions.all()
    return get_paginated_questions(request, questions, 'tag.html', {'tag_name': tag_name})

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, question=question)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.save()
            return redirect(f'{request.path}#answer-{answer.id}')
    else:
        form = AnswerForm()

    return render(request, 'question.html', {'question': question, 'answers': answers, 'form': form})

def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('login')
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()
            return redirect('question_detail', question_id=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404
