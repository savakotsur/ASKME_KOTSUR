from django.shortcuts import render
from .utils import paginate 

def get_questions_list():
    questions = []
    for i in range(1, 31):  # Заглушка для 30 вопросов
        questions.append({
            'title': f'Title {i}',
            'id': i,
            'text': f'Text {i}',
            'answers_count': 5, 
            'tags': ['tag1', 'tag2'] 
        })
    return questions

def index(request):
    questions = get_questions_list()
    per_page = 10

    page_obj = paginate(questions, request, per_page)

    return render(request, 'index.html', {'page_obj': page_obj})

def hot(request):
    questions = get_questions_list()
    per_page = 10

    page_obj = paginate(questions, request, per_page)

    return render(request, 'hot.html', {'page_obj': page_obj})

def tag_questions(request, tag_name):
    questions = get_questions_list()
    per_page = 10

    page_obj = paginate(questions, request, per_page)

    return render(request, 'tag.html', {'page_obj': page_obj, 'tag_name': tag_name})

def question_detail(request, question_id):
    question = {
        'title': f'Question {question_id}',
        'id': question_id,
        'text': f'Detailed text of question {question_id}'
    }
    answers = [
        {'id': 1, 'text': 'Answer 1 to question ' + str(question_id)},
        {'id': 2, 'text': 'Answer 2 to question ' + str(question_id)},
    ]
    return render(request, 'question.html', {'question': question, 'answers': answers})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def settings(request):
    return render(request, 'settings.html')
