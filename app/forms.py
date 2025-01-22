from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Question, Answer, Tag
from django.core.exceptions import ValidationError

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=40, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('No user found with this email.')
        return email

class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=40)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            self.add_error('repeat_password', 'Passwords do not match.') 
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        user = User.objects.create_user(
            username=cleaned_data['username'],
            email=cleaned_data['email'],
            password=cleaned_data['password']
        )

        profile = Profile.objects.create(user=user, avatar=cleaned_data['avatar'])
        return user

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    username = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        if self.cleaned_data['username'] and self.cleaned_data['username'] != user.username:
            user.username = self.cleaned_data['username']

        if self.cleaned_data['email'] and self.cleaned_data['email'] != user.email:
            user.email = self.cleaned_data['email']

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            profile.save()

        return profile

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, label='Tags', help_text='Enter tags separated by commas.')

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_tags(self):
        tag_names = self.cleaned_data['tags'].split(',')
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            tags.append(tag)
        return tags

    def save(self, commit=True, user=None):
        question = super().save(commit=False)
        if user:
            question.user = user 
        if commit:
            question.save()
            self.save_m2m()
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.question = self.question
        if commit:
            answer.save()
        return answer