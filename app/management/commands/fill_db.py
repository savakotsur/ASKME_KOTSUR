from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        # Создание пользователей и профилей
        self.stdout.write(self.style.SUCCESS(f'Создаём {ratio} пользователей'))
        for _ in range(ratio):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password='password123',
            )
            Profile.objects.create(user=user, avatar='avatars/default.png')

        # Создание тегов
        self.stdout.write(self.style.SUCCESS(f'Создаём {ratio} тегов'))
        tags = [Tag.objects.create(name=fake.unique.word()) for _ in range(ratio)]

        # Создание вопросов
        self.stdout.write(self.style.SUCCESS(f'Создаём {ratio * 10} вопросов'))
        questions = []
        for _ in range(ratio * 10):
            user = random.choice(User.objects.all())
            question = Question.objects.create(
                title=fake.sentence(),
                author=user,
                text=fake.text(),
                likes_count=random.randint(0, 100)
            )
            question.tags.set(random.sample(tags, random.randint(1, 3)))  # Добавляем случайные теги
            questions.append(question)

        # Создание ответов
        self.stdout.write(self.style.SUCCESS(f'Создаём {ratio * 100} ответов'))
        for _ in range(ratio * 100):
            user = random.choice(User.objects.all())
            question = random.choice(questions)
            Answer.objects.create(
                author=user,
                question=question,
                text=fake.text()
            )

        # Создание лайков и дизлайков на вопросы
        self.stdout.write(self.style.SUCCESS(f'Создаём {ratio * 200} лайков и дизлайков на вопросы'))
        for _ in range(ratio * 200):
            user = random.choice(User.objects.all())
            question = random.choice(questions)
            if random.choice([True, False]):
                question.liked_by.add(user)
                question.likes_count += 1
            else:
                question.disliked_by.add(user)
            question.save()

        # # Создание лайков на ответы
        # self.stdout.write(self.style.SUCCESS(f'Создаём {ratio * 200} лайков на ответы'))
        # answers = Answer.objects.all()
        # for _ in range(ratio * 200):
        #     user = random.choice(User.objects.all())
        #     answer = random.choice(answers)
        #     AnswerLike.objects.get_or_create(
        #         user=user,
        #         answer=answer,
        #         defaults={'is_liked': random.choice([True, False])}
        #     )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
