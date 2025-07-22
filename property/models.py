from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='property/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000)
    location = models.ForeignKey("Location", related_name="property_location", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="property_category", on_delete=models.CASCADE)
    create_at = models.DateTimeField(default= timezone.now)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('property:property_detail', kwargs={'slug': self.slug})


class PropertyImage(models.Model):
    property= models.ForeignKey("Property", related_name= "property_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return str(self.property.name)

class Location(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='locations/')

    def __str__(self):
        return str(self.name)

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)
    

class PropertyReview(models.Model):
    property = models.ForeignKey("Property", related_name='review_property', on_delete=models.CASCADE)
    user = models.ForeignKey( User, related_name='review_user', on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"review_{self.user.username}_{self.property.name}"
    

COUNT = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)
class PropertyBooking(models.Model):
    property = models.ForeignKey("Property", related_name='booking_property', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='booking_user', on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=timezone.now)
    date_from = models.DateField()
    date_to = models.DateField()
    guest = models.CharField(max_length=2 , choices=COUNT, default='1')
    children = models.CharField(max_length=2, choices=COUNT, default='0')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"booking_{self.user.username}_{self.property.name}"
    

