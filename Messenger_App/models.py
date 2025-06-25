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
    
    def get_active_avatar(self):
        return self.avatar_set.filter(active=True).first()
    def get_avatar_url(self):
        active_avatar_instance = self.get_active_avatar()
        
        if active_avatar_instance and active_avatar_instance.image and active_avatar_instance.image.file:
            return active_avatar_instance.image.file.url

        return static('images/avatar.png')


    def __str__(self):
        return self.user.username

class Avatar(models.Model):
    image = models.OneToOneField('Posts_app.Image', on_delete=models.CASCADE, related_name='avatar')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Аватар для профілю {self.profile}'

class Friendship(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_sent_request')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_accepted_request')
    accepted = models.BooleanField(default=False)
    def __str__(self):
        return f'Дружба між {self.profile1} та {self.profile2}'

class VerificationCode(models.Model):
    username = models.CharField(max_length=150)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Profile, blank=True)
    is_personal_chat = models.BooleanField(default=False)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='administered_group', null=True)
    avatar = models.ImageField(upload_to='images/group_avatars', blank=True, null=True)
    
    def __str__(self):
        return f'Група "{self.name}"'
        
    def get_members_ids(self):
        """Возвращает список ID всех пользователей в группе."""
        return list(self.members.values_list('user__id', flat=True))


class ChatMessage(models.Model):
    content = models.TextField(max_length=4096, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    attached_image = models.ImageField(upload_to='images/messages', blank=True, null=True)
    
    def __str__(self):
        return f'Повідомлення від {self.author}. Відправлено {self.sent_at}'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()