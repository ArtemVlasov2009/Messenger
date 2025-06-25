from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label="Тема публікації (Тег)",
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'tag-checkbox-list'
        }),
        required=False
    )
    
    article_link = forms.URLField(
        label="Посилання на статтю",
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.example.com',
            'class': 'form-control'
        })
    )

    images_upload = forms.FileField(
        label="Зображення",
        required=False,
        widget=forms.widgets.Input(attrs={
            'type': 'file',
            'multiple': True,
            'id': 'id_images_upload_input'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'article_link']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Природа, книга і спокій 🌿',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Інколи найкращі ідеї народжуються в тиші...',
                'class': 'form-control',
                'rows': 4
            }),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        return tags