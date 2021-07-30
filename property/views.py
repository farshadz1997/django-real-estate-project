from django.shortcuts import render
from .models import Property
import random
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.
def Home_Page(request):
    properties = Property.objects.all().order_by('-pub_date')[:6] # get last 6 items by publish date
    context = {
        "properties": properties,
    }
    return render(request, 'property/index.html', context)

class PropertiesList(ListView):
    model = Property
    template_name = 'property/properties-list.html'
    context_object_name = 'properties'
    ordering = ['-pub_date']
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_properties'] = Property.objects.order_by('-views')[:3]
        return context
    
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property/properties-detail.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nearby_properties'] = Property.objects.order_by('?').filter(city=self.object.city.lower()).exclude(id=self.object.id)[:2]
        context['popular_properties'] = Property.objects.order_by('-views').exclude(id=self.object.id)[:3]
        return context
    
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj