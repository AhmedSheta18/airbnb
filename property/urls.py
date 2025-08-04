from django.urls import path
from .views import PropertyList, PropertyDetail, AddProperty, EditProperty

app_name = 'property'

urlpatterns = [
    path('', PropertyList.as_view(), name='property_list'),
    path('add/', AddProperty.as_view(), name='add_property'),
    path('edit/<slug:slug>/', EditProperty.as_view(), name='edit_property'),
    path('<slug:slug>/', PropertyDetail.as_view(), name='property_detail'),
]