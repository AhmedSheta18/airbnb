from django import forms
from .models import PropertyBooking

class PropertyBookingForm(forms.ModelForm):
    class Meta:
        model = PropertyBooking
        fields = ['date_from', 'date_to', 'guest','children']