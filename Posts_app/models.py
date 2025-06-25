from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Image(models.Model):
    file = models.ImageField(upload_to='images/post_images/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('Messenger_App.Profile', on_delete=models.CASCADE, related_name='owned_images')
    
    def __str__(self):
        return self.filename

class Album(models.Model):
    name_of_album = models.CharField(max_length=255)
    theme_of_album = models.CharField(max_length=255, blank=True, null=True)
    year_of_album = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('Messenger_App.Profile', on_delete=models.CASCADE, related_name='albums')
    images = models.ManyToManyField(Image, blank=True, related_name='image_albums')
    preview_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='album_preview')
    
    def __str__(self):
        return self.name_of_album

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