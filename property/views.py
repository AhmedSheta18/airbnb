from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Property, PropertyImage, Location, Category, PropertyReview
# Create your views here.

class PropertyList(ListView):
    model = Property
    #! filter

class PropertyDetail(DetailView):
    model = Property
    #! booking 
