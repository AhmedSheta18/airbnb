from django.contrib import admin
from .models import Property, PropertyImage, Location, Category, PropertyReview, PropertyBooking    

# Register your models here.
admin.site.register(Property)
admin.site.register(PropertyImage)  
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(PropertyReview)
admin.site.register(PropertyBooking)