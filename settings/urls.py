from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home_index'),
    path('search/', views.home_search, name='home_search'),
    path('category/<slug:category>/', views.category_filter, name='category_filter'),
    path('location/<slug:location>/', views.location_filter, name='location_filter'),
    path('contact_us/',views.contact_us, name='contact_us')
]