from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path ('',views.Faqs.as_view(),name='about_list'),
]


