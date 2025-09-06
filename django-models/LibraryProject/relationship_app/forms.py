from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Include the fields you want users to fill
        fields = ['title', 'author']
