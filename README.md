# 🌐 Соціальна мережа "World IT" <a id="top"></a>

**World IT** — це амбітний проект, спрямований на створення повноцінної та функціональної соціальної мережі. Наша мета — реалізувати ключовий функціонал сучасних платформ, забезпечуючи комфортне спілкування, обмін контентом та можливість знаходити нових друзів. Проект розроблено з використанням сучасних технологій та модульної архітектури, що забезпечує гнучкість і масштабованість.

## 📑 Зміст

- [Ключові можливості](#key-features)
- [Стек технологій](#tech-stack)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Інструменти розробки](#dev-tools)
- [Запуск проекту локально](#local-setup)
- [Архітектура проекту](#architecture)
  - [Основні моделі даних](#data-models)
- [Дизайн та проектування](#design)
- [Команда розробників](#team)
- [Приклади коду](#code-examples)
  - [Реєстрація користувача](#registration)
  - [Модель для збереження коду підтвердження](#reg-code-model)
  - [Створення постів](#posts)
  - [Моделі для постів](#post-models)
  - [Чати в реальному часі](#chats)
  - [Frontend-логіка чатів](#chat-frontend)
  - [Моделі для чатів](#chat-models)
  - [Моделі профілю та друзів](#profile-models)
  - [Форми додатку (Django Forms)](#app-forms)
  - [Покращення інтерфейсу чату (JavaScript)](#chat-ui-js)
  - [Маршрутизація WebSocket](#ws-routing)
- [Висновок](#conclusion)

## ✨ Ключові можливості <a id="key-features"></a>

- ✅ **Реєстрація та автентифікація:** Безпечна система створення акаунтів із підтвердженням через email та входу.
- 👤 **Профілі користувачів:** Персоналізовані сторінки з можливістю налаштування аватарів, інформації про себе та управління контентом.
- 📝 **Стрічка новин та пости:** Створення, редагування, перегляд, лайки, коментарі та підтримка мультимедійного контенту (зображення, посилання).
- 💬 **Месенджер у реальному часі:** Приватні та групові чати з підтримкою WebSocket, включаючи відправку тексту та зображень.
- 👥 **Система друзів:** Додавання та видалення друзів, перегляд їх списків і управління соціальними зв’язками.

## 🛠️ Стек технологій <a id="tech-stack"></a>

Проект побудовано на основі сучасного технологічного стеку, що забезпечує продуктивність і зручність розробки.

### Backend <a id="backend"></a>
- **🐍 Python**: Основна мова програмування для серверної логіки.
- **🚀 Django**: Веб-фреймворк для швидкої розробки та управління проєктом.
- **🕸️ Django Channels (WebSocket)**: Реалізація чатів і сповіщень у реальному часі.
- **🗃️ SQLite**: Легковагова база даних для розробки та тестування (з можливістю переходу на PostgreSQL у продакшені).
- **📧 Django Email**: Відправка листів для підтвердження реєстрації та інших повідомлень.

### Frontend <a id="frontend"></a>
- **🌐 HTML**: Структура веб-сторінок.
- **🎨 CSS**: Стилізація інтерфейсу з адаптивним дизайном.
- **💻 JavaScript**: Інтерактивність і динамічний контент.
- **⚡️ AJAX**: Асинхронні запити для оновлення контенту без перезавантаження сторінок.
- **📚 jQuery**: Спрощення роботи з DOM та обробки подій.

### Інструменти розробки <a id="dev-tools"></a>
- **Git**: Контроль версій коду.
- **Figma/FigJam**: Проектування дизайну та архітектури.

## 🚀 Запуск проекту локально <a id="local-setup"></a>

Щоб запустити проєкт на своєму комп’ютері, виконайте наступні кроки:

1. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/ArtemVlasov2009/Messenger
   ```

2. **Перейдіть у директорію проєкту:**
   ```bash
   cd Messenger
   ```

3. **Створіть та активуйте віртуальне середовище:**
   - Для Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Для macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Застосуйте міграції бази даних:**
   ```bash
   python manage.py migrate
   ```

6. **Запустіть сервер для розробки:**
   ```bash
   python manage.py runserver
   ```

7. **Готово! 🎉** Відкрийте браузер і перейдіть за адресою: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## 🏗️ Архітектура проєкту <a id="architecture"></a>

Проєкт має модульну структуру, що складається з кількох Django-застосунків для чіткого поділу функціоналу:

- **`Messenger`**: Основний застосунок, що відповідає за маршрутизацію та інтеграцію компонентів.
- **`Messenger_App`**: Логіка месенджера, включаючи чати в реальному часі через WebSocket.
- **`Posts_app`**: Управління постами, включаючи створення, редагування, лайки та коментарі.
- **`Registration_app`**: Реєстрація, автентифікація, підтвердження email та відновлення пароля.

### Основні моделі даних <a id="data-models"></a>
- **User/Profile**: Управління користувачами та їх профілями.
- **Post/Link/Tag**: Створення та зберігання постів із тегами та посиланнями.
- **ChatGroup/ChatMessage**: Організація групових і особистих чатів із повідомленнями.
- **Send_Reg_Code**: Зберігання кодів підтвердження для реєстрації.

## 🎨 Дизайн та проектування <a id="design"></a>

- **[Архітектура (FigJam)](https://www.figma.com/board/bycCpq8bEEEHIMJLJyHarF/Untitled?node-id=0-1&t=tGh7GTL6TOhXgk7b-1)**: Схема взаємодії компонентів та логіки проєкту.
- **[Дизайн (Figma)](https://www.figma.com/design/20TZphWNufeAQYOe7E1sze/%D0%A1%D0%BE%D1%86%D1%96%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0-%D0%BC%D0%B5%D1%80%D0%B5%D0%B6%D0%B0-World-IT?node-id=6-26&t=6FcZEGOAfhm7mSQr-1)**: Макети інтерфейсу з адаптивним дизайном для всіх пристроїв.

## 👨‍💻 Команда розробників <a id="team"></a>

- **Власов Артем** — Тімлід([GitHub](https://github.com/ArtemVlasov2009/Messenger)).
- **Ткач Богдан** — ([GitHub](https://github.com/Bogdantkach12/Messenger_project)).
- **Іван Єжов** — ([GitHub](https://github.com/EzhovIvan)).

## 📖 Приклади коду <a id="code-examples"></a>

### Реєстрація користувача <a id="registration"></a>

Реєстрація включає відправку 6-значного коду підтвердження на email.

<details>
<summary>Переглянути код та пояснення</summary>

```python
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import RegistrationForm, CodeConfirmationForm, AuthorizationForm
from .models import Send_Reg_Code
import secrets
import string
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class RegistrationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__
        context['title'] = 'Реєстрація'
        context['subtitle'] = 'Приєднуйся до World IT'
        context['view_type'] = 'registration'
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        code = ''.join(secrets.choice(string.digits) for _ in range(6))

        self.request.session['registration_email'] = email
        self.request.session['registration_password'] = password
        self.request.session['verification_code'] = code

        Send_Reg_Code.objects.update_or_create(
            email=email,
            defaults={
                'code': code,
                'expires_at': timezone.now() + timezone.timedelta(minutes=15)
            }
        )

        try:
            subject = '✅ Підтвердіть свою електронну адресу для World IT Messenger!'
            message_body = f"""
Вітаємо у World IT Messenger! 👋

Будь ласка, використайте наступний код для підтвердження вашої електронної адреси:

{code}

Введіть цей код на сторінці підтвердження, щоб завершити реєстрацію. Код дійсний 15 хвилин.

Дякуємо за приєднання!
Команда World IT Messenger 🚀
"""
            send_mail(
                subject=subject,
                message=message_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
            messages.success(self.request, 'Код підтвердження відправлено на вашу пошту.')
            logger.info(f"Verification code sent to {email}")
            return redirect('confirm_code')
        except Exception as e:
            logger.error(f"Error sending email to {email}: {e}")
            messages.error(self.request, 'Виникла помилка при відправленні коду. Спробуйте ще раз або зверніться до підтримки.')
            self._cleanup_session()
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning(f"Invalid registration form: {form.errors}")
        self._cleanup_session()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def _cleanup_session(self):
        session_keys = ['registration_email', 'registration_password', 'verification_code']
        for key in session_keys:
            self.request.session.pop(key, None)
```

**Пояснення:**
- **Клас `RegistrationView`**: Використовує Django `FormView` для обробки форми реєстрації.
- **Генерація коду**: Створюється 6-значний код за допомогою `secrets` для безпеки.
- **Сесія**: Email, пароль і код зберігаються в сесії для подальшого використання.
- **Відправка email**: Використовується `send_mail` для надсилання коду підтвердження.
- **Логування**: Використовується `logging` для відстеження подій і помилок.
- **Очищення сесії**: Метод `_cleanup_session` видаляє тимчасові дані в разі помилки.

</details>

### Модель для збереження коду підтвердження <a id="reg-code-model"></a>

Зберігає код підтвердження для реєстрації.

<details>
<summary>Переглянути код та пояснення</summary>

```python
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Send_Reg_Code(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=15))
```

**Пояснення:**
- **Поле `email`**: Унікальне поле для зберігання адреси користувача.
- **Поле `code`**: Зберігає 6-значний код підтвердження.
- **Поле `expires_at`**: Вказує термін дії коду (15 хвилин).
- **Модель**: Використовується для тимчасового зберігання коду в базі даних.

</details>

### Створення постів <a id="posts"></a>

Підтримка тексту, зображень, посилань і тегів.

<details>
<summary>Переглянути код та пояснення</summary>

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Post, Link, Image
from .forms import PostForm
from Messenger_App.models import Profile
import logging

logger = logging.getLogger(__name__)

class PostsPageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'Posts_app/Posts.html'
    context_object_name = 'user_posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'posts'
        context['form'] = context.get('form', PostForm())
        return context

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = get_object_or_404(Profile, user=request.user)
            post.save()
            form.save_m2m()
            uploaded_images = request.FILES.getlist('images_upload')
            for f in uploaded_images:
                image_instance = Image.objects.create(file=f, owner=post.author, filename=f.name)
                post.images.add(image_instance)
            
            article_link = form.cleaned_data.get('article_link')
            if article_link:
                Link.objects.create(url=article_link, post=post)

            for key, value in request.POST.items():
                if key.startswith('extra_link_') and value.strip():
                    Link.objects.create(url=value.strip(), post=post)

            if is_ajax:
                return JsonResponse({'status': 'success', 'message': 'Пост успішно створено.'})
            return redirect('posts_page')
```

**Пояснення:**
- **Клас `PostsPageView`**: Комбінує `ListView` для відображення постів і обробку POST-запитів для їх створення.
- **Обробка файлів**: Підтримує завантаження кількох зображень через `request.FILES`.
- **Посилання**: Додає основне посилання (`article_link`) та додаткові посилання (`extra_link_`).
- **AJAX**: Використовується для асинхронного створення постів із JSON-відповідями.
- **Авторизація**: `LoginRequiredMixin` забезпечує доступ лише для авторизованих користувачів.

</details>

### Моделі для постів <a id="post-models"></a>

Зберігання постів, тегів і посилань.

<details>
<summary>Переглянути код та пояснення</summary>

```python
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey('Messenger_App.Profile', on_delete=models.CASCADE, related_name='posts_authored')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    
    def __str__(self):
        return self.title

class Link(models.Model):
    url = models.URLField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='links')
    
    def __str__(self):
        return self.url

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
```

**Пояснення:**
- **Модель `Post`**: Зберігає заголовок, вміст, автора, теги, зображення та дату створення.
- **Модель `Link`**: Зберігає URL-посилання, пов’язані з постом.
- **Модель `Tag`**: Унікальні теги для категоризації постів.
- **Зв’язки**: Використовуються `ForeignKey` і `ManyToManyField` для зв’язків між моделями.

</details>

### Чати в реальному часі <a id="chats"></a>

Реалізація через WebSocket.

<details>
<summary>Переглянути код та пояснення</summary>

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatGroup, ChatMessage, Profile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_pk']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.chat_group = await self.get_group_if_member(self.user, self.room_name)
        if not self.chat_group:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get('message', '')

        if not message_content.strip():
            return

        author_profile = await self.get_user_profile(self.user)
        if not author_profile:
            return

        avatar_url = await self.get_avatar_url(author_profile)
        message = await self.save_message_to_db(author_profile, self.chat_group, message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'username': self.user.username,
                'author_first_name': self.user.first_name,
                'author_avatar_url': avatar_url,
                'sent_at': message.sent_at.isoformat(),
                'image_url': None,
                'is_personal': self.chat_group.is_personal_chat
            }
        )
```

**Пояснення:**
- **Клас `ChatConsumer`**: Використовує `AsyncWebsocketConsumer` для обробки WebSocket-з’єднань.
- **Автентифікація**: Перевіряє, чи користувач авторизований і є членом чату.
- **Повідомлення**: Зберігає повідомлення в базі та надсилає їх усім учасникам чату через `group_send`.
- **Асинхронність**: Використовує `database_sync_to_async` для безпечного доступу до бази даних.

</details>

### Frontend-логіка чатів <a id="chat-frontend"></a>

Обробка повідомлень на клієнтській стороні.

<details>
<summary>Переглянути код та пояснення</summary>

```javascript
const webSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${groupPk}/`);
webSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type !== 'chat') return;
    const isSentByMe = data.username === currentUsername;
    const messageClass = isSentByMe ? 'sent' : 'received';
    let messageContentHtml = '';
    if (data.message) { messageContentHtml += `${data.message.replace(/\n/g, '<br>')}`; }
    if (data.image_url) { messageContentHtml += `<a href="${data.image_url}" target="_blank"><img src="${data.image_url}" alt="Attached image"></a>`; }
    let authorHtml = '';
    if (!isSentByMe && document.querySelector('.message-author')) { authorHtml = `<div class="message-author">${data.username}</div>`; }
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', messageClass);
    messageDiv.innerHTML = `<div class="message-body"><div class="message-content">${messageContentHtml}</div><span class="message-time">${formatTime(data.sent_at)}</span></div>`;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
};
```

**Пояснення:**
- **WebSocket**: Встановлює з’єднання з сервером для отримання повідомлень у реальному часі.
- **Обробка повідомлень**: Додає отримані повідомлення до DOM із відповідними стилями (`sent` або `received`).
- **Підтримка зображень**: Відображає вкладені зображення як посилання з попереднім переглядом.
- **Автоскрол**: Прокручує контейнер повідомлень донизу після додавання нового повідомлення.

</details>

### Моделі для чатів <a id="chat-models"></a>

Зберігання групових і особистих чатів.

<details>
<summary>Переглянути код та пояснення</summary>

```python
class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Profile, blank=True)
    is_personal_chat = models.BooleanField(default=False)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='administered_group', null=True)
    avatar = models.ImageField(upload_to='images/group_avatars', blank=True, null=True)
    
    def __str__(self):
        return f'Група "{self.name}"'

class ChatMessage(models.Model):
    content = models.TextField(max_length=4096, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    attached_image = models.ImageField(upload_to='images/messages', blank=True, null=True)
    
    def __str__(self):
        return f'Повідомлення від {self.author}. Відправлено {self.sent_at}'
```

**Пояснення:**
- **Модель `ChatGroup`**: Зберігає інформацію про групу, її учасників, адміністратора та аватар.
- **Модель `ChatMessage`**: Зберігає текст повідомлення, автора, групу, дату відправлення та вкладене зображення.
- **Поля**: Використовуються `ManyToManyField` для учасників і `ImageField` для зображень.
- **Логіка**: Підтримує як особисті, так і групові чати через поле `is_personal_chat`.

</details>

### Моделі профілю та друзів <a id="profile-models"></a>
Ці моделі розширюють стандартну модель `User` і реалізують систему дружби.

<details>
<summary>Переглянути код та пояснення</summary>

```python
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static 

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    signature = models.ImageField(upload_to='images/signatures', blank=True, null=True)
    
    def get_avatar_url(self):
        active_avatar_instance = self.avatar_set.filter(active=True).first()
        if active_avatar_instance and active_avatar_instance.image and active_avatar_instance.image.file:
            return active_avatar_instance.image.file.url
        return static('images/avatar.png')

    def __str__(self):
        return self.user.username

class Avatar(models.Model):
    image = models.OneToOneField('Posts_app.Image', on_delete=models.CASCADE, related_name='avatar')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class Friendship(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_sent_request')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_accepted_request')
    accepted = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

**Пояснення:**
- **Модель `Profile`**: Розширює стандартну модель `User` за допомогою `OneToOneField`. Зберігає додаткові дані, як-от дата народження та підпис. Метод `get_avatar_url` повертає URL активного аватара або стандартне зображення.
- **Модель `Avatar`**: Пов'язує профіль (`Profile`) із завантаженим зображенням (`Image`) та позначає його як активний.
- **Модель `Friendship`**: Реалізує систему запитів у друзі. Зберігає зв'язок між двома профілями та статус (`accepted`), що вказує, чи прийнято запит.
- **Сигнали `post_save`**: Автоматично створюють `Profile` для кожного нового `User` (`create_user_profile`) та зберігають його при оновленні `User` (`save_user_profile`), забезпечуючи цілісність даних.

</details>

### Форми додатку (Django Forms) <a id="app-forms"></a>
Форми є ключовим елементом взаємодії з користувачем, від авторизації до налаштувань профілю.

<details>
<summary>Переглянути код та пояснення</summary>

```python
from django import forms
from django.contrib.auth.models import User
from .models import Profile, ChatMessage

class SettingsForm(forms.ModelForm):
    """Форма для страницы настроек пользователя."""
    first_name = forms.CharField(label="Ім’я", max_length=30, required=True)
    last_name = forms.CharField(label="Прізвище", max_length=30, required=True)
    email = forms.EmailField(label="Електронна пошта", required=True)
    date_of_birth = forms.DateField(label="Дата народження", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    password = forms.CharField(label="Новий пароль", widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(label="Підтвердіть новий пароль", widget=forms.PasswordInput, required=False)

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
```
**Пояснення:**
- **Клас `SettingsForm`**: Це `ModelForm`, що дозволяє редагувати дані моделі `User`. Він включає поля для зміни імені, прізвища та email. Також додано поля для зміни пароля з валідацією в методі `clean()`, яка перевіряє, чи паролі співпадають і чи відповідають вимогам безпеки.
- **Клас `MessageForm`**: `ModelForm` для створення повідомлень у чаті (`ChatMessage`). Використовує віджет `Textarea` для зручного введення тексту та дозволяє прикріпити зображення.

</details>

### Покращення інтерфейсу чату (JavaScript) <a id="chat-ui-js"></a>
JavaScript використовується для покращення користувацького досвіду, наприклад, для автоматичного скролінгу та зміни розміру поля вводу.

<details>
<summary>Переглянути код та пояснення</summary>

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const messagesDisplay = document.getElementById('messages-display');
    if (messagesDisplay) {
        messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
    }

    const textarea = document.querySelector('.message-input-area .message-textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto'; 
            this.style.height = (this.scrollHeight) + 'px'; 
        });
        textarea.style.height = (textarea.scrollHeight) + 'px';
    }

    if (textarea) {
        textarea.focus();
    }
});
```
**Пояснення:**
- **`DOMContentLoaded`**: Скрипт виконується після повного завантаження структури сторінки.
- **Автоматичне прокручування**: Знаходить контейнер з повідомленнями (`messages-display`) і прокручує його до самого низу, щоб користувач одразу бачив останні повідомлення.
- **Динамічний розмір поля вводу**: Для елемента `textarea` додається слухач події `input`. При введенні тексту висота поля автоматично змінюється відповідно до вмісту, що робить введення довгих повідомлень зручнішим.
- **Фокус на полі вводу**: Автоматично встановлює фокус на полі для введення повідомлення, дозволяючи користувачеві одразу почати друкувати.

</details>

### Маршрутизація WebSocket <a id="ws-routing"></a>
Для роботи чатів у реальному часі необхідно налаштувати маршрути для WebSocket-з'єднань.

<details>
<summary>Переглянути код та пояснення</summary>

```python
from django.urls import path 
from .consumers import ChatConsumer

ws_urlpatterns = [
    path('ws/chat/<int:group_pk>/', ChatConsumer.as_asgi()),
]
```
**Пояснення:**
- **`ws_urlpatterns`**: Цей список містить маршрути для WebSocket. Його підключають до основного файлу маршрутизації ASGI-додатку.
- **`path('ws/chat/<int:group_pk>/', ...)`**: Визначає URL-шаблон для WebSocket-з'єднання.
  - `ws/`: Стандартний префікс для WebSocket.
  - `chat/`: Вказує, що це маршрут для чату.
  - `<int:group_pk>/`: Динамічний сегмент, що приймає ID групи чату. Це дозволяє одному консьюмеру обслуговувати безліч чатів.
- **`ChatConsumer.as_asgi()`**: Вказує, що всі з'єднання за цим маршрутом буде обробляти клас `ChatConsumer`.

</details>

## 📝 Висновок <a id="conclusion"></a>

Розробка цього проекту стала важливим етапом у нашому професійному зростанні. Ми здобули цінний досвід у створенні складних веб-додатків з нуля, опанували сучасні технології та навчилися ефективно працювати в команді. Проєкт допоміг нам:

- Поглибити знання **Django**, включаючи Django Channels для WebSocket.
- Поліпшити навички роботи з **JavaScript**, **AJAX**, **HTML** і **CSS**.
- Розвинути вміння проектувати модульну архітектуру та створювати адаптивний дизайн.
- Зрозуміти, як масштабувати проєкти та інтегрувати різні технології.

Ці навички стануть основою для наших майбутніх проєктів, адже використані технології є затребуваними на ринку IT.
