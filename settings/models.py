from django.db import models

# Create your models here.
class Settings(models.Model):
    site_name = models.CharField(max_length=100, default='My Site')
    logo = models.ImageField(upload_to='site_logos/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.site_name