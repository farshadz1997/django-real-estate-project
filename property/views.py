from django.shortcuts import render
from .models import Property, Category
from django.db.models import F
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
    categories = Category.objects.all()
    location = request.GET.get('location')
    category = request.GET.get('category')
    look_for = request.GET.get('look_for')
    context = {
        "properties": properties,
        "location": location,
        "categories": categories,
        "look_for": look_for,
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
        context['categories'] = Category.objects.all()
        return context
 
    
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property/properties-detail.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nearby_properties'] = Property.objects.order_by('?').filter(city=self.object.city.lower()).exclude(id=self.object.pk)[:2]
        context['popular_properties'] = Property.objects.order_by('-views').exclude(id=self.object.pk)[:3]
        context['categories'] = Category.objects.all()
        return context
    
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj
    
class SearchView(ListView):
    model = Property
    template_name = 'property/properties-list.html'
    context_object_name = 'properties'
    ordering = ['-pub_date']
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_properties'] = Property.objects.order_by('-views')[:3]
        context['categories'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        location = self.request.GET.get('location')
        category = self.request.GET.get('category')
        look_for = self.request.GET.get('look_for')
        if location and category and look_for:
            object_list = Property.objects.filter(city__icontains = location, category__slug = category, property_status = look_for)
        elif location and category:
            object_list = Property.objects.filter(city__icontains = location, category__slug = category)
        elif location and look_for:
            object_list = Property.objects.filter(city__icontains = location, property_status = look_for)
        elif category and look_for:
            object_list = Property.objects.filter(category__slug = category, property_status = look_for)
        elif look_for:
            object_list = Property.objects.filter(property_status = look_for)
        elif location:
            object_list = Property.objects.filter(city__icontains = location)
        elif category:
            object_list = Property.objects.filter(category__slug = category)
        else:
            object_list = Property.objects.all()
        return object_list