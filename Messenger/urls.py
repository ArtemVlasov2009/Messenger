from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Registration_app.views import CustomLogoutView, RegistrationView, CodeConfirmationView, AuthorizationView
from Messenger_App.views import (
    MessengerPageView, SettingsView, FriendsView, delete_photo, delete_post, edit_post,
    ProfileView, ChatsView, ChatView, redirect_to_personal_chat, confirm_friend_request,
    delete_friend_request, delete_friend, create_group_chat, upload_chat_image,
    edit_group_chat, add_members_to_chat, get_group_members, remove_group_member,
    delete_group_chat
)
from Posts_app.views import PostsPageView, delete_link

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Головна сторінка
    path('', MessengerPageView.as_view(), name='messenger_page'),
    path('messenger/', MessengerPageView.as_view(), name='messenger'),
    
    # Реєстрація та Авторизація
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('confirm_code/', CodeConfirmationView.as_view(), name='confirm_code'),
    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    
    # Пости
    path('posts/', PostsPageView.as_view(), name='posts_page'),
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('posts/edit/<int:post_id>/', edit_post, name='edit_post'),
    path('posts/delete_link/<int:post_id>/', delete_link, name='delete_link'),
    
    # Налаштування та Профіль
    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/delete_photo/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    
    # Друзі
    path('friends/', FriendsView.as_view(), name='friends'),
    path('confirm_friend_request/<int:user_id>/', confirm_friend_request, name='confirm_friend_request'),
    path('delete_friend_request/<int:user_id>/', delete_friend_request, name='delete_friend_request'),
    path('delete_friend/<int:user_id>/', delete_friend, name='delete_friend'),
    
    # Чати
    path('chats/', ChatsView.as_view(), name='chats'),
    path('chat/<int:group_pk>/', ChatView.as_view(), name='chat'),
    path('chat/upload_image/', upload_chat_image, name='upload_chat_image'),
    path('to_personal_chat/<int:user2_pk>/', redirect_to_personal_chat, name='to_personal_chat'), # <-- Ось правильне ім'я
    path('create_group_chat/', create_group_chat, name='create_group_chat'),
    path('chat/edit/<int:group_pk>/', edit_group_chat, name='edit_group_chat'),
    path('chat/add_members/<int:group_pk>/', add_members_to_chat, name='add_members_to_chat'),
    path('chat/get_members/<int:group_pk>/', get_group_members, name='get_group_members'),
    path('chat/remove_member/<int:group_pk>/<int:user_pk>/', remove_group_member, name='remove_group_member'),
    path('chat/delete/<int:group_pk>/', delete_group_chat, name='delete_chat')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)