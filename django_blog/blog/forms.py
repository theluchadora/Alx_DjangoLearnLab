from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post, Tag

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
    tags_field = forms.CharField(
        required=False,
        help_text='Separate tags with commas (e.g. django, python)',
        widget=forms.TextInput()
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_field']

    def __init__(self, *args, **kwargs):
        # If editing existing post, populate tags_field with existing tags
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags_field'].initial = ', '.join(t.name for t in self.instance.tags.all())
