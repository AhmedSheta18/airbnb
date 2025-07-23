from django.contrib import admin
from .models import Property, PropertyImage, Location, Category, PropertyReview, PropertyBooking    
from django_summernote.admin import SummernoteModelAdmin

# Apply summernote to all TextField in model.
class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'location', 'category', 'create_at')
    list_display_links = ('name','price', 'location', )
    list_editable = ('category',)
    search_fields = ('name', 'location__name', 'category__name')
    list_filter = ('category', 'location','price')
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Property, PropertyAdmin)
# admin.site.register(Property, SomeModelAdmin)
admin.site.register(PropertyImage)  
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(PropertyReview, SomeModelAdmin)
admin.site.register(PropertyBooking)






