from django import forms
from .models import User_Post

from django import forms
from .models import User_Post

class PostForm(forms.ModelForm):
    class Meta:
        model = User_Post
        fields = ['title', 'theme', 'text', 'article_link']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Назва публікації',
                'class': 'form-control'
            }),
            'theme': forms.TextInput(attrs={
                'placeholder': 'Напишіть тему публікації',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Поділіться своїми думками...',
                'class': 'form-control',
                'rows': 5
            }),
            'article_link': forms.URLInput(attrs={
                'placeholder': 'https://www.instagram.com/...',
                'class': 'form-control'
            }),
        }
