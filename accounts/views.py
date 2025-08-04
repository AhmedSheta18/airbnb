from django.shortcuts import get_object_or_404, redirect, render
from .models import Profile
from .forms import UserForm , ProfileForm , UserCreateForm
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from property.models import Property, PropertyBooking, PropertyReview, PropertyImage
from property.forms import PropertyReviewForm
from django.http import Http404
# Create your views here.

def signup(request):
    if request.method == 'POST':
        signup_form = UserCreateForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            # return redirect(reverse('login'))
            username = signup_form.cleaned_data['username']
            password = signup_form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect(reverse('accounts:profile'))
    
    else:
        signup_form = UserCreateForm()

    return render(request,'registration/signup.html',{'signup_form':signup_form})



@login_required(login_url='login')
def profile(request):
    profile = Profile.objects.get(user = request.user)
    return render(request,'profile/profile.html',{'profile':profile})



@login_required(login_url='login')
def profile_edit(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST , instance=request.user)
        profile_form = ProfileForm(request.POST , request.FILES , instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            my_form = profile_form.save(commit=False)
            my_form.user = request.user
            my_form.save()
            messages.success(request, 'Profile details updated.')
            return redirect(reverse('accounts:profile'))
    
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance = profile)       

    return render(request,'profile/profile_edit.html',{
        'user_form' : user_form , 
        'profile_form' : profile_form
    })



def my_reservation(request):
    now = timezone.now().date()
    
    user_reservation = PropertyBooking.objects.filter(user=request.user)
    
    # Get all properties that the user has booked
    booked_properties = user_reservation.values_list('property', flat=True).distinct()
    
    # Get all reviews by the user for these properties
    user_reviews = PropertyReview.objects.filter(user=request.user, property__in=booked_properties)
    
    # Create a dictionary of property_id -> review for quick lookup
    reviewed_properties = {review.property_id: review for review in user_reviews}
    
    # Add a 'has_review' flag to each reservation
    for reservation in user_reservation:
        reservation.has_review = reservation.property_id in reviewed_properties
        if reservation.has_review:
            reservation.review = reviewed_properties[reservation.property_id]
    
    return render(request, 'profile/my_reservation.html', {
        'user_reservation': user_reservation,
        'now': now,
    })


@login_required(login_url='login')
def add_feedback(request, slug):
    property = get_object_or_404(Property, slug=slug)
    
    # Check if user has already reviewed this property
    try:
        user_feedback = PropertyReview.objects.get(property=property, user=request.user)
        is_update = True
    except PropertyReview.DoesNotExist:
        user_feedback = None
        is_update = False
    
    if request.method == 'POST':
        if is_update:
            form = PropertyReviewForm(request.POST, instance=user_feedback)
            success_message = 'Your review has been updated successfully!'
        else:
            form = PropertyReviewForm(request.POST)
            success_message = 'Thank you for your review!'
            
        if form.is_valid():
            myform = form.save(commit=False)
            myform.property = property
            myform.user = request.user
            myform.save()
            messages.success(request, success_message)
            return redirect('accounts:my_reservation')
    else:
        if is_update:
            form = PropertyReviewForm(instance=user_feedback)
        else:
            form = PropertyReviewForm()
    
    context = {
        'form': form,
        'property': property,
        'is_update': is_update
    }
    return render(request, 'profile/property_feedback.html', context)


def custom_logout(request):
    print("Custom logout view called")
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


@login_required(login_url='login')
def my_properties(request):
    from django.utils import timezone
    now = timezone.now().date()
    
    # Get all properties owned by the user
    user_properties = Property.objects.filter(owner=request.user)
    
    # Get booking statistics for each property
    for prop in user_properties:
        prop.total_bookings = PropertyBooking.objects.filter(property=prop).count()
        prop.active_bookings = PropertyBooking.objects.filter(
            property=prop, 
            date_from__lte=now, 
            date_to__gte=now
        ).count()
        prop.upcoming_bookings = PropertyBooking.objects.filter(
            property=prop, 
            date_from__gt=now
        ).count()
        prop.completed_bookings = PropertyBooking.objects.filter(
            property=prop, 
            date_to__lt=now
        ).count()
        
        # Get additional images
        prop.additional_images = PropertyImage.objects.filter(property=prop)
    
    return render(request, 'profile/my_properties.html', {
        'user_properties': user_properties,
        'now': now,
    })


'''
        if request.method == 'POST':
            form = PropertyReviewForm(request.POST , instance=user_feedback)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.property = property
                myform.author = request.user
                myform.save()

        else:
            form = PropertyReviewForm(instance=user_feedback)
        return render(request,'profile/property_feedback.html' , {'form':form , 'property':property})

        '''

@login_required(login_url='login')
def booking_details(request, booking_id):
    from django.utils import timezone
    now = timezone.now().date()
    
    try:
        # Get the booking and ensure it belongs to the current user
        booking = get_object_or_404(PropertyBooking, id=booking_id)
        
        if booking.user != request.user:
            raise Http404("You don't have permission to view this booking.")
        
        # Check if user has already reviewed this property
        try:
            user_review = PropertyReview.objects.get(property=booking.property, user=request.user)
            booking.has_review = True
            booking.review = user_review
        except PropertyReview.DoesNotExist:
            booking.has_review = False
            booking.review = None
        
        # Get additional property images
        property_images = PropertyImage.objects.filter(property=booking.property)
        
        context = {
            'booking': booking,
            'property_images': property_images,
            'now': now,
        }
        
        return render(request, 'profile/booking_details.html', context)
    
    except PropertyBooking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('accounts:my_reservation')