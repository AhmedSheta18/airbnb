from django.shortcuts import render
from .models import Settings
from property.models import Property, Location, Category
from blog.models import Post
from django.db.models import Count
from django.db.models.query_utils import Q
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    """
    Render the home page.
    """
    room_list = Property.objects.filter(category__name='room')[:4]
    resturant_list = Property.objects.filter(category__name='restaurant')[:4]
    hotel_list = Property.objects.filter(category__name='hotel')[:5]

    posts = Post.objects.all()[:4]

    user_count = User.objects.all().count()
    room_count = Property.objects.filter(category__name='room').count()
    resturant_count = Property.objects.filter(category__name='restaurant').count()
    hotel_count = Property.objects.filter(category__name='hotel').count()
    
    return render(request, 'home/home_index.html', {
        'locations': Location.objects.all().annotate(property_count=Count('property_location')),  
        'categories': Category.objects.all().annotate(post_count=Count('property_category')),
        'hotel_list': hotel_list,
        'room_list': room_list,
        'resturant_list': resturant_list,
        'posts': posts,
        'user_count': user_count,
        'room_count': room_count,
        'hotel_count': hotel_count,
        'resturant_count': resturant_count
    })



def home_search(request):
    """
    Handle search functionality on the home page.
    """
    keyword_search = request.GET.get('keyword_search', '')
    place_search = request.GET.get('place', '')

    property_list = Property.objects.filter(
        (Q(name__icontains=keyword_search) | Q(description__icontains=keyword_search)) &
        Q(location__name__icontains=place_search)
    )
    return render(request, 'home/home_search.html', {
        'property_list': property_list,
    })


def category_filter(request, category):
    """
    Filter properties by category.
    """
    category = Category.objects.get( name = category)
    # properties = Property.objects.filter(
    #     Q(category__name__icontains=category) 
    # )
    properties = Property.objects.filter(category=category)
    return render(request, 'home/home_search.html', {
        'property_list': properties,
    })


def location_filter(request, location):
    """
    Filter properties by location.
    """
    location = Location.objects.get(name=location)
    properties = Property.objects.filter(location=location)
    return render(request, 'home/home_search.html', {
        'property_list': properties,
    })


def contact_us(request):
    return render(request,'home\contact.html', {"contact": Settings.objects.last()})
