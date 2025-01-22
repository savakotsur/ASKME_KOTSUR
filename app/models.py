from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars/', default='media/avatars/default.png', blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def popular(self):
        return self.order_by('-likes_count')
        
class Question(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_questions", blank=True)
    disliked_by = models.ManyToManyField(User, related_name="disliked_questions", blank=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_answers', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_answers', blank=True)
    likes_count = models.IntegerField(default=0)
