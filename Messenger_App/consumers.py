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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

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

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'author_first_name': event.get('author_first_name', ''),
            'author_avatar_url': event.get('author_avatar_url'),
            'sent_at': event['sent_at'],
            'image_url': event.get('image_url'),
            'is_personal': event.get('is_personal', False)
        }))

    @database_sync_to_async
    def get_group_if_member(self, user, group_pk):
        try:
            group = ChatGroup.objects.get(pk=group_pk)
            if group.members.filter(user=user).exists():
                return group
        except ChatGroup.DoesNotExist:
            pass
        return None

    @database_sync_to_async
    def get_user_profile(self, user):
        try:
            return Profile.objects.select_related('user').get(user=user)
        except Profile.DoesNotExist:
            return None

    @database_sync_to_async
    def get_avatar_url(self, profile):
        if not profile:
            return None
        
        active_avatar = profile.get_active_avatar()
        
        if active_avatar and hasattr(active_avatar, 'image') and active_avatar.image and hasattr(active_avatar.image, 'file'):
            return active_avatar.image.file.url
        
        return None

    @database_sync_to_async
    def save_message_to_db(self, author_profile, chat_group, message_content: str):
        message = ChatMessage.objects.create(
            content=message_content,
            author=author_profile,
            chat_group=chat_group
        )
        return message