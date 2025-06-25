from django import forms
from django.contrib.auth.models import User

from Posts_app.models import Album, Image, Post, Tag, Link
from .models import Profile, ChatGroup, ChatMessage


class AuthorizationForm(forms.Form):
    """Форма для страницы авторизации."""
    email = forms.EmailField(
        label="Електронна пошта",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your_email@example.com'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'})
    )

class ModalActionForm(forms.Form):
    """Форма для модального окна редактирования базовой информации пользователя."""
    name = forms.CharField(max_length=100, label="Ім’я")
    surname = forms.CharField(max_length=100, label="Прізвище")
    login = forms.CharField(max_length=100, label="Логін")

class SettingsForm(forms.ModelForm):
    """Форма для страницы настроек пользователя."""
    first_name = forms.CharField(
        label="Ім’я",
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label="Прізвище",
        max_length=30,
        required=True
    )
    email = forms.EmailField(
        label="Електронна пошта",
        required=True
    )
    date_of_birth = forms.DateField(
        label="Дата народження",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    password = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput,
        required=False
    )
    password_confirm = forms.CharField(
        label="Підтвердіть новий пароль",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', 'Паролі не співпадають.')
            if len(password) < 8:
                self.add_error('password', 'Пароль повинен містити щонайменше 8 символів.')
        elif password or password_confirm:
            self.add_error(None, 'Заповніть обидва поля пароля.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Ім’я"
        self.fields['last_name'].label = "Прізвище"
        self.fields['email'].label = "Електронна пошта"

class ImageForm(forms.ModelForm):
    """Форма для загрузки одного изображения."""
    class Meta:
        model = Image
        fields = ['file']
        labels = {
            'file': 'Файл зображення'
        }

class MessageForm(forms.ModelForm):
    """Форма для отправки сообщения в чате."""
    class Meta:
        model = ChatMessage
        fields = ['content', 'attached_image']
        labels = {
            'content': 'Ваше повідомлення',
            'attached_image': 'Прикріпити зображення'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть повідомлення...'}),
        }

class PasswordChangeCodeForm(forms.Form):
    """Форма для ввода кода подтверждения смены пароля."""
    code = forms.CharField(
        label="Код підтвердження",
        max_length=6,
        required=True
    )

class PostForm(forms.ModelForm):
    """Форма для создания и редактирования поста."""
    article_link = forms.URLField(
        label="Посилання на статтю",
        required=False
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'images']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст посту',
            'tags': 'Теги',
            'images': 'Зображення'
        }

class AlbumForm(forms.ModelForm):
    """Форма для создания и редактирования альбома."""
    class Meta:
        model = Album

        fields = ['name_of_album', 'theme_of_album', 'year_of_album']
        

        labels = {
            'name_of_album': 'Назва альбому',
            'theme_of_album': 'Тема альбому',
            'year_of_album': 'Рік альбому',
        }
        

        widgets = {
            'name_of_album': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'theme_of_album': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_album': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
