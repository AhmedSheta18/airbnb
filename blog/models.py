from django.urls import reverse
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
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
