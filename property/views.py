from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormMixin, CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Property, PropertyImage, Location, Category, PropertyReview, PropertyBooking
from .forms import PropertyBookingForm, PropertyForm, PropertyImageFormSet
from .filters import PropertyFilter
from django_filters.views import FilterView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.

class PropertyList(FilterView):
    model = Property
    paginate_by = 6
    filterset_class = PropertyFilter
    template_name = 'property/property_list.html'
    #! filter

class PropertyDetail(FormMixin, DetailView):
    model = Property
    form_class = PropertyBookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Property.objects.filter(category = self.get_object().category).exclude(id=self.get_object().id)[:3]
        
        # Get all bookings for this property to determine unavailable dates
        property_bookings = PropertyBooking.objects.filter(property=self.get_object())
        booked_dates = []
        
        # Create a list of all booked date ranges
        for booking in property_bookings:
            # Convert dates to string format for JavaScript
            booked_dates.append({
                'start': booking.date_from.strftime('%Y-%m-%d'),
                'end': booking.date_to.strftime('%Y-%m-%d')
            })
        
        context['booked_dates'] = booked_dates
        return context
    
    def post(self, request, *args, **kwargs):
        # Clear any existing messages to prevent duplication
        storage = messages.get_messages(request)
        for _ in storage:
            pass  # Iterate through to mark all existing messages as read
        
        form = self.get_form()
        if form.is_valid():
            # Check if the dates are available
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            property_obj = self.get_object()
            
            # Check for overlapping bookings
            overlapping_bookings = PropertyBooking.objects.filter(
                property=property_obj,
                date_from__lte=date_to,
                date_to__gte=date_from
            ).exists()
            
            if overlapping_bookings:
                messages.error(request, 'Sorry, the property is not available for the selected dates. Please choose different dates.')
                return self.form_invalid(form)
            
            # If dates are available, proceed with booking
            myform = form.save(commit=False)
            myform.property = property_obj
            myform.user = request.user
            myform.total_price = (myform.date_to - myform.date_from).days * property_obj.price
            myform.save()
            messages.success(request, 'Booking confirmed successfully!')
            return redirect('property:property_list')
        else:
            return self.form_invalid(form)


class AddProperty(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/add_property.html'
    success_url = reverse_lazy('property:property_list')
    login_url = '/accounts/login/'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Property added successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PropertyImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = PropertyImageFormSet()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = PropertyImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)
    
    def form_valid(self, form, formset):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        formset.instance = self.object
        formset.save()
        messages.success(self.request, 'Property added successfully!')
        return redirect(self.get_success_url())
    
    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class EditProperty(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/edit_property.html'
    login_url = '/accounts/login/'
    
    def get_success_url(self):
        return reverse('property:property_detail', kwargs={'slug': self.object.slug})
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PropertyImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PropertyImageFormSet(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)
    
    def form_valid(self, form, formset):
        form.save()
        formset.save()
        messages.success(self.request, 'Property updated successfully!')
        return redirect(self.get_success_url())
    
    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


# {% for image in object.property_image.all %}
#     <div class="item">
#         <div class="hotel-img" style="background-image: url({% static 'image.url'%});"></div>
#     </div>
# {% endfor %}