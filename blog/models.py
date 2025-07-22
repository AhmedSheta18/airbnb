from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    author = models.ForeignKey(User,related_name='post_author' ,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tags = TaggableManager()
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=15000)
    category = models.ForeignKey('Category', related_name='post_category', on_delete=models.CASCADE)
    comments = models.ManyToManyField(User, related_name='post_comments', blank=True)
    slug = models.SlugField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_at']


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
