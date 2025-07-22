from django.db import models

# Create your models here.

class About(models.Model):
    what_we_do = models.TextField(max_length=1000, blank=True, null=True)
    our_mission = models.TextField(max_length=1000, blank=True, null=True)
    our_goals = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='about_images/')

    def __str__(self):
        return f'About Us - {self.id}'
    

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=1000)

    def __str__(self):
        return self.question
