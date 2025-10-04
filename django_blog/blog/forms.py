from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post
from taggit.forms import TagWidget

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']  # Add 'first_name', 'last_name' if you want

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ['content']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),
        }