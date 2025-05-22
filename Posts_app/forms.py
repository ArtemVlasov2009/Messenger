from django import forms
from .models import User_Post  

class PostForm(forms.ModelForm):
    tags = forms.ChoiceField(choices=User_Post.TAG_CHOICES,
                             label="Тема публікації",
                             widget=forms.Select(attrs={
                                 'class': 'form-control'
                             }))

    image1 = forms.ImageField(label="Додати фото",
                              required=False,
                              widget=forms.ClearableFileInput(attrs={
                                  'class': 'form-control-file'
                              }))

    class Meta:
        model = User_Post
        fields = ['title', 'theme', 'tags', 'text', 'article_link', 'image1']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Природа, книга і спокій 🌿',
                'class': 'form-control'
            }),
            'theme': forms.TextInput(attrs={
                'placeholder': 'Тема публікації',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Інколи найкращі ідеї народжуються в тиші. Природа, книга і спокій — усе, що потрібно, аби перезавантажитись. #відпочинок #натхнення #життя #природа #читання #спокій #гармонія',
                'class': 'form-control',
                'rows': 4
            }),
            'article_link': forms.URLInput(attrs={
                'placeholder': 'https://www.instagram.com/world.it.acad...',
                'class': 'form-control'
            }),
        }
