from django import forms
from django.utils import timezone
from .models import PropertyBooking, PropertyReview, Property, PropertyImage

class PropertyBookingForm(forms.ModelForm):
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Check-in Date',
            'autocomplete': 'off',
            'data-provide': 'datepicker',
            'data-date-format': 'yyyy-mm-dd',
            'data-date-autoclose': 'true'
        })
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Check-out Date',
            'autocomplete': 'off',
            'data-provide': 'datepicker',
            'data-date-format': 'yyyy-mm-dd',
            'data-date-autoclose': 'true'
        })
    )
    
    class Meta:
        model = PropertyBooking
        fields = ['date_from', 'date_to', 'guest', 'children']
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to:
            # Check if check-in date is in the past
            if date_from < timezone.now().date():
                self.add_error('date_from', 'Check-in date cannot be in the past.')
            
            # Check if check-out date is before check-in date
            if date_to <= date_from:
                self.add_error('date_to', 'Check-out date must be after check-in date.')
            
            # Check if the stay is too long (e.g., more than 30 days)
            if (date_to - date_from).days > 30:
                self.add_error('date_to', 'Booking cannot exceed 30 days.')
        
        return cleaned_data


class PropertyReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rate from 1 to 5',
            'min': '1',
            'max': '5'
        })
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Share your experience with this property',
            'rows': '5'
        })
    )
    
    class Meta:
        model = PropertyReview
        fields = ['rating', 'comment']
        
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")
        return rating


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'price', 'description', 'location', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price per night'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Property Description', 'rows': '5'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

PropertyImageFormSet = forms.inlineformset_factory(
    Property, PropertyImage, form=PropertyImageForm,
    extra=3, can_delete=True
)