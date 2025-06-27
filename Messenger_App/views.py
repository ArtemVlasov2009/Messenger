from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from .forms import (
    AuthorizationForm, ModalActionForm, SettingsForm, AlbumForm, ImageForm,
    MessageForm, PasswordChangeCodeForm, PostForm
)
from Posts_app.models import Album, Image, Post, Tag, Link
from .models import Profile, Avatar, ChatGroup, ChatMessage, Friendship
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.db.models import Prefetch, OuterRef, Subquery
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

class MessengerPageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'Messenger_App/Messenger.html'
    context_object_name = 'user_posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_profile = self.request.user.profile
        context['current_page'] = 'messenger'
        context['post_form'] = context.get('post_form', PostForm())
        context['modal_form'] = ModalActionForm(initial={
            'name': self.request.user.first_name,
            'surname': self.request.user.last_name,
            'login': self.request.user.username
        })

        friendship_requests = Friendship.objects.filter(
            profile2=current_user_profile, accepted=False
        ).select_related(
            'profile1__user'
        ).prefetch_related(
            Prefetch(
                'profile1__avatar_set',
                queryset=Avatar.objects.filter(active=True).select_related('image'),
                to_attr='active_avatars'
            )
        )[:3]

        friend_requests_data = []
        for fr in friendship_requests:
            requesting_profile = fr.profile1
            avatar = requesting_profile.active_avatars[0] if hasattr(requesting_profile, 'active_avatars') and requesting_profile.active_avatars else None
            friend_requests_data.append({
                'user': requesting_profile.user,
                'avatar': avatar,
            })
        context['friend_requests_data'] = friend_requests_data

        personal_chat_ids = list(ChatGroup.objects.filter(
            members=current_user_profile,
            is_personal_chat=True
        ).values_list('id', flat=True))

        if personal_chat_ids:
            latest_message_subquery = ChatMessage.objects.filter(
                chat_group=OuterRef('chat_group_id')
            ).order_by('-sent_at').values('id')[:1]

            latest_messages = ChatMessage.objects.filter(
                chat_group_id__in=personal_chat_ids,
                id=Subquery(latest_message_subquery)
            ).select_related(
                'chat_group',
                'author__user'
            ).prefetch_related(
                'chat_group__members__user',
                Prefetch(
                    'chat_group__members__avatar_set',
                    queryset=Avatar.objects.filter(active=True).select_related('image'),
                    to_attr='active_avatars'
                )
            ).order_by('-sent_at')[:3]

            recent_personal_chats = []
            for message in latest_messages:
                chat = message.chat_group
                other_member = next((m for m in chat.members.all() if m != current_user_profile), None)
                if other_member:
                    other_member_avatar = other_member.active_avatars[0] if hasattr(other_member, 'active_avatars') and other_member.active_avatars else None
                    recent_personal_chats.append({
                        'other_member': other_member,
                        'last_message': message,
                        'other_member_avatar': other_member_avatar,
                    })
            context['recent_personal_chats'] = recent_personal_chats
        else:
            context['recent_personal_chats'] = []

        context['persons'] = User.objects.exclude(pk=self.request.user.pk)
        context['group_chats'] = ChatGroup.objects.filter(members=current_user_profile)
        
        users = User.objects.all().select_related('profile').exclude(pk=self.request.user.pk)
        user_data = []
        for user in users:
            active_avatar = None
            if hasattr(user, 'profile'):
                active_avatar = Avatar.objects.filter(profile=user.profile, active=True).select_related('image').first()
            user_data.append({'user': user, 'avatar': active_avatar})
        context['all_users'] = user_data

        return context

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if 'content' in request.POST:
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
                return redirect('messenger')
            else:
                if is_ajax:
                    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
                
                self.object_list = self.get_queryset()
                context = self.get_context_data(object_list=self.object_list)
                context['post_form'] = form
                return self.render_to_response(context)

        modal_form = ModalActionForm(request.POST)
        if modal_form.is_valid():
            user = request.user
            user.first_name = modal_form.cleaned_data['name']
            user.last_name = modal_form.cleaned_data['surname']
            user.username = modal_form.cleaned_data['login']
            user.save()
            return redirect('messenger')

        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        context['modal_form'] = modal_form
        return self.render_to_response(context)


class ChatView(LoginRequiredMixin, View):
    template_name = 'Messenger_App/chat_detail.html'

    def get(self, request, *args, **kwargs):
        group_pk = self.kwargs.get('group_pk')
        chat_group = get_object_or_404(ChatGroup, pk=group_pk)
        
        current_profile = get_object_or_404(Profile, user=request.user)
        if current_profile not in chat_group.members.all():
            return HttpResponseForbidden('<h1>У Вас немає доступу до цього чату</h1>')
        
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}
        group_pk = self.kwargs.get('group_pk')
        current_user_profile = get_object_or_404(Profile, user=self.request.user)
        
        context['chat_group'] = get_object_or_404(ChatGroup.objects.prefetch_related('members__user'), pk=group_pk)
        context['current_page'] = 'chats'

        message_history = ChatMessage.objects.filter(
            chat_group_id=group_pk
        ).select_related(
            'author__user'
        ).prefetch_related(
            Prefetch(
                'author__avatar_set',
                queryset=Avatar.objects.filter(active=True).select_related('image'),
                to_attr='active_avatar_list'
            )
        ).order_by('sent_at')

        for message in message_history:
            if hasattr(message.author, 'active_avatar_list') and message.author.active_avatar_list:
                message.author_active_avatar = message.author.active_avatar_list[0]
            else:
                message.author_active_avatar = None
        
        context['message_history'] = message_history

        users = User.objects.all().select_related('profile').exclude(pk=self.request.user.pk)
        user_data = []
        for user in users:
            active_avatar = Avatar.objects.filter(profile=user.profile, active=True).select_related('image').first()
            user_data.append({'user': user, 'avatar': active_avatar})
        context['all_users'] = user_data

        context['group_chats'] = ChatGroup.objects.filter(
            members=current_user_profile, is_personal_chat=False
        ).order_by('-id')
        
        personal_chats_query = ChatGroup.objects.filter(
            members=current_user_profile,
            is_personal_chat=True
        ).prefetch_related('members__user').order_by('-id')

        personal_chats_data = []
        for chat in personal_chats_query:
            other_member = next((member for member in chat.members.all() if member != current_user_profile), None)
            if other_member:
                avatar = Avatar.objects.filter(profile=other_member, active=True).select_related('image').first()
                avatar_url = avatar.image.file.url if avatar and avatar.image and hasattr(avatar.image, 'file') else None
                personal_chats_data.append({
                    'chat_pk': chat.pk,
                    'other_user_name': f"{other_member.user.first_name} {other_member.user.last_name}",
                    'other_user_avatar_url': avatar_url
                })
        context['personal_chats'] = personal_chats_data
        
        return context

@login_required
def redirect_to_personal_chat(request, user2_pk):
    user1_profile = get_object_or_404(Profile, user=request.user)
    user2_profile = get_object_or_404(Profile, user_id=user2_pk)

    group = ChatGroup.objects.annotate(
        num_members=models.Count('members')
    ).filter(
        is_personal_chat=True,
        members=user1_profile
    ).filter(
        members=user2_profile
    ).filter(num_members=2).first()

    if not group:
        group = ChatGroup.objects.create(
            name=f'Персональний чат між {user1_profile.user.username} та {user2_profile.user.username}',
            is_personal_chat=True,
            admin=user1_profile
        )
        group.members.add(user1_profile, user2_profile)
    return redirect('chat', group_pk=group.pk)

@login_required
def create_group_chat(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        member_ids = request.POST.getlist('members')
        avatar_file = request.FILES.get('avatar')

        if not group_name or not member_ids:
            return JsonResponse({'success': False, 'error': 'Назва групи та вибір хоча б одного учасника є обов\'язковими.'}, status=400)

        group = ChatGroup.objects.create(
            name=group_name,
            admin=request.user.profile,
            is_personal_chat=False,
            avatar=avatar_file
        )
        
        group.members.add(request.user.profile)
        
        for member_id in member_ids:
            try:
                if int(member_id) != request.user.id:
                    profile = Profile.objects.get(user_id=member_id)
                    group.members.add(profile)
            except (Profile.DoesNotExist, ValueError):
                pass
        
        return JsonResponse({'success': True, 'chat_url': f'/chat/{group.pk}/'})

    return JsonResponse({'success': False, 'error': 'Неправильний метод запиту.'}, status=400)

@login_required
def upload_chat_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        group_pk = request.POST.get('group_pk')
        message_content = request.POST.get('message', '')

        if not image_file or not group_pk:
            return JsonResponse({'success': False, 'error': 'Файл або ID групи відсутні.'}, status=400)

        chat_group = get_object_or_404(ChatGroup, pk=group_pk)
        author_profile = get_object_or_404(Profile, user=request.user)

        if author_profile not in chat_group.members.all():
            return JsonResponse({'success': False, 'error': 'Ви не є учасником цього чату.'}, status=403)

        message = ChatMessage.objects.create(
            author=author_profile,
            chat_group=chat_group,
            attached_image=image_file,
            content=message_content
        )

        active_avatar = author_profile.get_active_avatar()
        avatar_url = None
        if active_avatar and active_avatar.image and hasattr(active_avatar.image, 'file'):
            avatar_url = active_avatar.image.file.url

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{group_pk}",
            {
                'type': 'chat_message',
                'message': message.content,
                'username': message.author.user.username,
                'author_first_name': message.author.user.first_name,
                'author_avatar_url': avatar_url,
                'sent_at': message.sent_at.isoformat(),
                'image_url': message.attached_image.url if message.attached_image else None,
                'is_personal': chat_group.is_personal_chat
            }
        )
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Неправильний метод запиту.'}, status=400)

@login_required
def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if post.author.user == request.user:
            post.delete()
            return JsonResponse({'status': 'success', 'message': 'Пост успішно видалено.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Ви не маєте права видаляти цей пост'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Невірний метод запиту'}, status=400)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Ви не маєте права редагувати цей пост'}, status=403)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()

            if 'file' in request.FILES:
                image_form = ImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    image = image_form.save()
                    post.images.add(image)

            Link.objects.filter(post=post).delete()
            article_link = form.cleaned_data.get('article_link')
            if article_link:
                Link.objects.create(url=article_link, post=post)

            return JsonResponse({'status': 'success', 'message': 'Пост успішно оновлено.'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        tags_list = list(post.tags.values_list('name', flat=True))
        links = Link.objects.filter(post=post)
        images = post.images.all()
        return JsonResponse({
            'status': 'success',
            'title': post.title,
            'content': post.content,
            'tags': tags_list,
            'article_link': links.first().url if links.exists() else '',
            'images': [image.file.url for image in images]
        })

@login_required
def delete_photo(request, photo_id):
    if request.method == 'POST':
        photo = get_object_or_404(Image, id=photo_id)
        if hasattr(photo, 'owner') and photo.owner.user == request.user:
            photo.delete()
            return JsonResponse({'status': 'success', 'message': 'Фото успішно видалено.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Ви не маєте права видаляти це фото.'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Невірний метод запиту.'}, status=400)

class AuthorizationView(View):
    def get(self, request):
        form = AuthorizationForm()
        return render(request, 'Messenger_App/authorization.html', {'form': form})

    def post(self, request):
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('messenger')
            else:
                form.add_error(None, 'Невірна електронна пошта або пароль.')
        return render(request, 'Messenger_App/authorization.html', {'form': form})

class CustomLogoutView(LogoutView):
    next_page = 'authorization'

class SettingsView(LoginRequiredMixin, View):
    template_name = 'Messenger_App/settings.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        context = {
            'user': user,
            'profile': profile,
            'current_page': 'settings',
            'photos': Image.objects.filter(owner=profile).order_by('-id'),
            'albums': Album.objects.filter(owner=profile).prefetch_related('images').distinct().order_by('-created_at'),
            'album_form': AlbumForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        
        action = request.POST.get('action')
        form_name = next((key for key in ['upload_photo_form', 'create_album_form', 'edit_album_form', 'album_photo_form'] if key in request.POST), None)

        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()

            photo_file = request.FILES.get('profile_photo')
            if photo_file:
                Avatar.objects.filter(profile=profile, active=True).update(active=False)
                new_image = Image.objects.create(owner=profile, file=photo_file)
                new_avatar = Avatar.objects.create(profile=profile, image=new_image, active=True)
                return JsonResponse({'success': True, 'photo_url': new_avatar.image.file.url})
            
            return JsonResponse({'success': True})

        elif action == 'update_info':
            errors = {}
            first_name = request.POST.get('name')
            last_name = request.POST.get('surname')
            email = request.POST.get('email')
            date_of_birth = request.POST.get('date_of_birth')

            if not first_name: errors['name'] = 'Ім\'я є обов\'язковим полем.'
            if not last_name: errors['surname'] = 'Прізвище є обов\'язковим полем.'
            if not email:
                errors['email'] = 'Email є обов\'язковим полем.'
            else:
                try:
                    validate_email(email)
                    if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                         errors['email'] = 'Цей email вже використовується.'
                except ValidationError:
                    errors['email'] = 'Введіть коректний email.'

            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email
            user.save()
            
            profile.date_of_birth = date_of_birth if date_of_birth else None
            profile.save()
            return JsonResponse({'success': True, 'new_data': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'user_tag': user.username
            }})

        elif action == 'request_password_code':
            password = request.POST.get('password')
            try:
                validate_password(password, user)
            except ValidationError as e:
                return JsonResponse({'success': False, 'errors': {'password': list(e.messages)}}, status=400)

            request.session['pending_password'] = password
            code = ''.join(secrets.choice(string.digits) for _ in range(6))
            request.session['password_change_code'] = code
            request.session['password_change_expiry'] = (timezone.now() + timedelta(minutes=10)).isoformat()
            
            send_mail('Код для зміни пароля', f'Ваш код для зміни пароля: {code}', settings.DEFAULT_FROM_EMAIL, [user.email])
            return JsonResponse({'success': True})

        elif action == 'confirm_change':
            code = request.POST.get('code')
            session_code = request.session.get('password_change_code')
            expiry_str = request.session.get('password_change_expiry')
            
            if not all([session_code, expiry_str]):
                return JsonResponse({'success': False, 'errors': 'Сесія застаріла. Спробуйте ще раз.'}, status=400)
            if timezone.now() > timezone.datetime.fromisoformat(expiry_str):
                return JsonResponse({'success': False, 'errors': 'Час дії коду вичерпано.'}, status=400)
            
            if code == session_code:
                user.set_password(request.session.get('pending_password'))
                user.save()
                update_session_auth_hash(request, user)
                del request.session['password_change_code']
                del request.session['password_change_expiry']
                del request.session['pending_password']
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': 'Невірний код підтвердження.'}, status=400)
        
        elif form_name == 'upload_photo_form':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.owner = profile
                image.save()
                return JsonResponse({'success': True, 'photo_id': image.id, 'photo_url': image.file.url})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif form_name == 'create_album_form':
            form = AlbumForm(request.POST)
            if form.is_valid():
                album = form.save(commit=False)
                album.owner = profile
                album.save()
                return JsonResponse({'success': True, 'album': {
                    'id': album.id,
                    'name_of_album': album.name_of_album,
                    'theme_of_album': album.theme_of_album,
                    'year_of_album': album.year_of_album,
                }})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif form_name == 'edit_album_form':
            album_id = request.POST.get('album_id')
            album = get_object_or_404(Album, id=album_id, owner=profile)
            form = AlbumForm(request.POST, instance=album)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        
        elif form_name == 'album_photo_form':
            album_id = request.POST.get('album_id')
            album = get_object_or_404(Album, id=album_id, owner=profile)
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.owner = profile
                image.save()
                album.images.add(image)
                return JsonResponse({'success': True, 'photo_id': image.id, 'photo_url': image.file.url})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        return JsonResponse({'success': False, 'errors': 'Невідома дія.'}, status=400)

class FriendsView(LoginRequiredMixin, View):
    template_name = 'Messenger_App/friends.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user

        all_users_qs = User.objects.exclude(pk=current_user.pk).select_related('profile')

        friendships_received = Friendship.objects.filter(profile2__user=current_user, accepted=False)
        request_users_qs = User.objects.filter(pk__in=friendships_received.values('profile1__user')).select_related('profile')

        friends_profiles = Friendship.objects.filter(
            models.Q(profile1__user=current_user, accepted=True) |
            models.Q(profile2__user=current_user, accepted=True)
        )
        friend_pks1 = friends_profiles.values_list('profile1__user__pk', flat=True)
        friend_pks2 = friends_profiles.values_list('profile2__user__pk', flat=True)
        friend_pks = set(list(friend_pks1) + list(friend_pks2))
        if current_user.pk in friend_pks:
            friend_pks.remove(current_user.pk)
        friends_qs = User.objects.filter(pk__in=list(friend_pks)).select_related('profile')

        def prepare_user_data(user_queryset):
            data_list = []
            for user in user_queryset:
                avatar = None
                if hasattr(user, 'profile'):
                    avatar = Avatar.objects.filter(profile=user.profile, active=True).select_related('image').first()
                avatar_url = avatar.image.file.url if avatar and avatar.image and hasattr(avatar.image, 'file') else None
                data_list.append({'user': user, 'avatar_url': avatar_url})
            return data_list

        context = {
            'current_page': 'friends',
            'recommendations_data': prepare_user_data(all_users_qs),
            'requests_data': prepare_user_data(request_users_qs),
            'friends_data': prepare_user_data(friends_qs),
        }
        return render(request, self.template_name, context)

@login_required
def confirm_friend_request(request, user_id):
    if request.method == 'POST':
        user_to_confirm = get_object_or_404(User, pk=user_id)
        friendship = get_object_or_404(Friendship, profile2__user=request.user, profile1__user=user_to_confirm, accepted=False)
        friendship.accepted = True
        friendship.save()

        profile = get_object_or_404(Profile, user=user_to_confirm)
        avatar = Avatar.objects.filter(profile=profile, active=True).first()
        profile_photo_url = avatar.image.file.url if avatar and avatar.image and hasattr(avatar.image, 'file') else '/static/images/Avatarka-user-11.svg'
        
        return JsonResponse({
            'success': True,
            'user_id': user_to_confirm.id,
            'username': f"{user_to_confirm.first_name} {user_to_confirm.last_name}",
            'user_tag': user_to_confirm.username,
            'profile_photo': profile_photo_url
        })
    return JsonResponse({'success': False}, status=400)

@login_required
def delete_friend_request(request, user_id):
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, pk=user_id)
        friendship = Friendship.objects.filter(
            (models.Q(profile1__user=request.user, profile2__user=user_to_delete) |
            models.Q(profile2__user=request.user, profile1__user=user_to_delete)),
            accepted=False
        ).first()
        if friendship:
            friendship.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Запит на дружбу не знайдено.'}, status=404)
    return JsonResponse({'success': False}, status=400)

@login_required
def delete_friend(request, user_id):
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, pk=user_id)
        friendship = Friendship.objects.filter(
            (models.Q(profile1__user=request.user, profile2__user=user_to_delete) |
            models.Q(profile2__user=request.user, profile1__user=user_to_delete)),
            accepted=True
        ).first()
        if friendship:
            friendship.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Друг не знайдений.'}, status=404)
    return JsonResponse({'success': False}, status=400)

class ProfileView(LoginRequiredMixin, View):
    template_name = 'Messenger_App/profile.html'

    def get(self, request, user_id, *args, **kwargs):
        profile_user = get_object_or_404(User, pk=user_id)
        profile = get_object_or_404(Profile, user=profile_user)
        posts = Post.objects.filter(author=profile).order_by('-id')
        albums = Album.objects.filter(owner=profile).distinct().order_by('-created_at')
        context = {
            'profile_user': profile_user,
            'current_page': 'profile',
            'posts': posts,
            'albums': albums,
        }
        return render(request, self.template_name, context)

class ChatsView(LoginRequiredMixin, View):
    template_name = 'Messenger_App/chats.html'

    def get(self, request, *args, **kwargs):
        current_user_profile = get_object_or_404(Profile, user=request.user)

        users_for_modal = User.objects.select_related('profile').exclude(pk=request.user.pk)
        all_users_data = []
        for user in users_for_modal:
            active_avatar = Avatar.objects.filter(profile=user.profile, active=True).select_related('image').first()
            all_users_data.append({
                'user': user,
                'avatar': active_avatar
            })

        group_chats_list = ChatGroup.objects.filter(
            members=current_user_profile,
            is_personal_chat=False
        ).order_by('-id')

        personal_chats_query = ChatGroup.objects.filter(
            members=current_user_profile,
            is_personal_chat=True
        ).prefetch_related('members__user', 'members__avatar_set__image').order_by('-id')

        personal_chats_data = []
        for chat in personal_chats_query:
            other_member = next((member for member in chat.members.all() if member != current_user_profile), None)
            
            if other_member:
                avatar = Avatar.objects.filter(profile=other_member, active=True).select_related('image').first()
                avatar_url = None
                if avatar and avatar.image and hasattr(avatar.image, 'file'):
                    avatar_url = avatar.image.file.url
                
                personal_chats_data.append({
                    'chat_pk': chat.pk,
                    'other_user_name': f"{other_member.user.first_name} {other_member.user.last_name}",
                    'other_user_avatar_url': avatar_url
                })

        context = {
            'current_page': 'chats',
            'group_chats': group_chats_list,
            'all_users': all_users_data,
            'personal_chats': personal_chats_data,
        }
        
        return render(request, self.template_name, context)

@login_required
def get_group_members(request, group_pk):
    group = get_object_or_404(ChatGroup, pk=group_pk)
    if request.user.profile not in group.members.all():
        return JsonResponse({'success': False, 'error': 'Доступ заборонено.'}, status=403)

    members_data = []
    admin_user = group.admin.user
    for profile in group.members.select_related('user').all():
        avatar = Avatar.objects.filter(profile=profile, active=True).select_related('image').first()
        avatar_url = avatar.image.file.url if avatar and avatar.image and hasattr(avatar.image, 'file') else None
        members_data.append({
            'id': profile.user.id,
            'name': f"{profile.user.first_name} {profile.user.last_name}",
            'avatar': avatar_url, 
            'is_admin': profile.user == admin_user
        })
    return JsonResponse({'success': True, 'members': members_data})

@login_required
def remove_group_member(request, group_pk, user_pk):
    if request.method == 'POST':
        group = get_object_or_404(ChatGroup, pk=group_pk)
        if group.admin.user != request.user:
            return JsonResponse({'success': False, 'error': 'Ви не є адміністратором цієї групи.'}, status=403)
        if group.admin.user.pk == int(user_pk):
            return JsonResponse({'success': False, 'error': 'Адміністратор не може видалити себе з групи.'}, status=400)

        member_to_remove = get_object_or_404(Profile, user__pk=user_pk)
        if member_to_remove in group.members.all():
            group.members.remove(member_to_remove)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Цей користувач не є учасником групи.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Неправильний метод запиту.'}, status=400)

@login_required
def edit_group_chat(request, group_pk):
    if request.method == 'POST':
        group = get_object_or_404(ChatGroup, pk=group_pk)
        if group.admin.user != request.user:
            return JsonResponse({'success': False, 'error': 'Ви не є адміністратором цієї групи.'}, status=403)

        group_name = request.POST.get('group_name')
        avatar_file = request.FILES.get('avatar')
        if group_name:
            group.name = group_name
        if avatar_file:
            group.avatar = avatar_file
        group.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Неправильний метод запиту.'}, status=400)

@login_required
def add_members_to_chat(request, group_pk):
    if request.method == 'POST':
        group = get_object_or_404(ChatGroup, pk=group_pk)
        if group.admin.user != request.user:
            return JsonResponse({'success': False, 'error': 'Ви не є адміністратором цієї групи.'}, status=403)

        member_ids = request.POST.getlist('members')
        if not member_ids:
            return JsonResponse({'success': False, 'error': 'Не вибрано жодного учасника.'}, status=400)
            
        for member_id in member_ids:
            try:
                profile_to_add = Profile.objects.get(user_id=int(member_id))
                group.members.add(profile_to_add)
            except (Profile.DoesNotExist, ValueError):
                continue
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Неправильний метод запиту.'}, status=400)

@login_required
def delete_group_chat(request, group_pk):
    if request.method == 'POST':
        group = get_object_or_404(ChatGroup, pk=group_pk)

        if group.admin.user != request.user:
            return JsonResponse({'success': False, 'error': 'Ви не є адміністратором цієї групи.'}, status=403)
        
        group.delete()
        
        redirect_url = reverse('chats')
        return JsonResponse({'success': True, 'redirect_url': redirect_url})

    return JsonResponse({'success': False, 'error': 'Неправильний метод запиту.'}, status=400)