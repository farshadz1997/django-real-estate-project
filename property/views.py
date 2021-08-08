from django.shortcuts import render
from .models import Property, Category
from django.db.models import Avg, Max, Min
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
    context = {
        "properties": properties,
        "categories": categories,
    }
    return render(request, 'property/index.html', context)

class PropertiesList(ListView):
    model = Property
    template_name = 'property/properties-list.html'
    context_object_name = 'properties'
    ordering = ['-pub_date']
    paginate_by = 6
    
    def get_context_data(self, *args, **kwargs):
        context = super(PropertiesList, self).get_context_data(*args, **kwargs)
        context['popular_properties'] = Property.objects.order_by('-views')[:3]
        context['categories'] = Category.objects.all()
        context['min_max_price'] = Property.objects.aggregate(maximum = Max('price'), minimum = Min('price'))
        context['current_order'] = self.request.GET.get('sort_by')
        context['current_pagination'] = self.get_paginate_by(self.paginate_by)
        return context
    
    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by) 
    
    def get_ordering(self):
        ordering = super(PropertiesList, self).get_ordering()
        if self.request.GET.get('sort_by') == "Name":
            self.get_paginate_by(self.paginate_by)
            return ('-title')
        elif self.request.GET.get('sort_by') == "Price":
            return ('-price')
        elif self.request.GET.get('sort_by') == "Date":
            return ('-pub_date')
        else:
            return self.ordering
 
    
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
    
    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['popular_properties'] = Property.objects.order_by('-views')[:3]
        context['categories'] = Category.objects.all()
        context['current_order'] = self.request.GET.get('sort_by')
        context['current_pagination'] = self.get_paginate_by(self.paginate_by)
        return context
    
    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by) 
    
    def get_ordering(self):
        ordering = super(SearchView, self).get_ordering()
        if self.request.GET.get('sort_by') == "Name":
            self.get_paginate_by(self.paginate_by)
            return ('-title')
        elif self.request.GET.get('sort_by') == "Price":
            return ('-price')
        elif self.request.GET.get('sort_by') == "Date":
            return ('-pub_date')
        else:
            return self.ordering
    
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
    
class GalleryView(ListView):
    model = Property
    template_name = 'property/gallery.html'
    context_object_name = 'property'
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(GalleryView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context
        