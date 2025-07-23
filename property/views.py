from django.shortcuts import render , redirect
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from .models import Property, PropertyImage, Location, Category, PropertyReview
from .forms import PropertyBookingForm
from .filters import PropertyFilter
from django_filters.views import FilterView

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
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.property = self.get_object()
            myform.user = request.user
            myform.total_price = (myform.date_to - myform.date_from).days * self.get_object().price
            myform.save()
            return redirect('property:property_list',)
        else:
            return self.form_invalid(form)
    



# {% for image in object.property_image.all %}
#     <div class="item">
#         <div class="hotel-img" style="background-image: url({% static 'image.url'%});"></div>
#     </div>
# {% endfor %}