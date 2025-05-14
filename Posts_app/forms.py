from django import forms
from .models import User_Post

class PostForm(forms.ModelForm):
    class Meta:
        model = User_Post
        fields = ['title', 'theme', 'tags', 'text', 'article_link', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9']
        