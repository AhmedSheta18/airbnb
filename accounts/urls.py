from django.urls import path
from .views import profile, profile_edit, signup, my_reservation, add_feedback, my_properties, booking_details
from accounts.views import custom_logout


app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    #this profile and edit profile are for the user
    path('profile/', profile, name='profile'),
    path('profile/edit', profile_edit, name='profile_edit'),
    # this is ia my booking page and booking details and review
    path('profile/booking', my_reservation, name='my_reservation'),
    path('profile/booking/<int:booking_id>/', booking_details, name='booking_details'),
    path('profile/booking/<slug:slug>/review', add_feedback, name='add_feedback'),
    # this is for the user to see their properties
    path('profile/properties', my_properties, name='my_properties'),
    # Custom logout view
    path('logout/', custom_logout, name='logout'),  
]
