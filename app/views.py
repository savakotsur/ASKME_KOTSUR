from django.shortcuts import render, get_object_or_404
from .utils import paginate  
from .models import Question, Tag, Answer
from django.conf.urls import handler404

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
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question=question)
    return render(request, 'question.html', {'question': question, 'answers': answers})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def settings(request):
    return render(request, 'settings.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404
