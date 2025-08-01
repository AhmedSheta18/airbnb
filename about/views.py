from django.shortcuts import render
from .models import About, FAQ
from django.views.generic import ListView
# Create your views here.


class Faqs(ListView):
    model = FAQ


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about"] = About.objects.last() 
        return context
    