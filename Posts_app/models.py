from django.db import models
from django.contrib.auth.models import User

class User_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    theme = models.CharField(max_length=255)
    TAG_CHOICES = [
        ('vacation', 'Відпочинок'),
        ('inspiration', 'Натхнення'),
        ('life', 'Життя'),
        ('nature', 'Природа'),
        ('reading', 'Читання'),
        ('calm', 'Спокій'),
        ('harmony', 'Гармонія'),
        ('music', 'Музика'),
        ('movies', 'Фільми'),
        ('travel', 'Подорожі'),
    ]
    tags = models.CharField(max_length=255, choices=TAG_CHOICES)
    text = models.TextField()
    article_link = models.URLField(blank=True, null=True)
    image1 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image6 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image7 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image8 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    image9 = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title