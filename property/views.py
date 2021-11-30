from django.db.models import query
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Property, Category
from blog.models import Blog
from django.db.models import Max, Min
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.http import Http404

# Create your views here.
def Home_Page(request):
    properties = Property.objects.all().order_by('-pub_date')[:6] # get last 6 items by publish date
    exclusive_properties = Property.objects.filter(status='Exc')
    categories = Category.objects.all()
    blogs = Blog.objects.all().order_by('-pub_date')[:3]
    property_choices = dict(Property.property_choices)
    context = {
        "properties": properties,
        "exclusive_properties": exclusive_properties,
        "categories": categories,
        "blogs": blogs,
        "property_choices": property_choices
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
        context['property_choices'] = dict(Property.property_choices)
        context['current_order'] = self.request.GET.get('sort_by')
        context['current_pagination'] = self.get_paginate_by(self.paginate_by)
        get_copy = self.request.GET.copy() 
        context['parameters'] = get_copy.pop('page', True) and get_copy.urlencode()
        return context
    
    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by) 
    
    def get_ordering(self):
        ordering = super(PropertiesList, self).get_ordering()
        if self.request.GET.get('sort_by') == "Name":
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
        context['nearby_properties'] = Property.objects.order_by('?').filter(city=self.object.city).exclude(id=self.object.pk)[:2]
        context['popular_properties'] = Property.objects.order_by('-views').exclude(id=self.object.pk)[:3]
        context['categories'] = Category.objects.all()
        context['property_choices'] = dict(Property.property_choices)
        return context
    
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

class UserPropertiesListView(ListView):
    model = Property
    template_name = 'property/properties-list.html'
    context_object_name = 'properties'
    paginate_by = 6
    
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Property.objects.filter(author=user).order_by('-pub_date')

class SearchView(ListView):
    model = Property
    template_name = 'property/properties-list.html'
    context_object_name = 'properties'
    ordering = '-pub_date'
    paginate_by = 6
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_properties'] = Property.objects.order_by('-views')[:3]
        context['categories'] = Category.objects.all()
        context['current_order'] = self.request.GET.get('sort_by')
        context['current_pagination'] = self.get_paginate_by(self.paginate_by)
        context['property_choices'] = dict(Property.property_choices)
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        return context
    
    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)
        
    def get_ordering(self):
        ordering = super(SearchView, self).get_ordering()
        if self.request.GET.get('sort_by') == "Name":
            return ('-title')
        elif self.request.GET.get('sort_by') == "Price":
            return ('-price')
        elif self.request.GET.get('sort_by') == "Date":
            return ('-pub_date')
        else:
            return self.ordering
    
    def get_queryset(self):
        location = self.request.GET.get('location', None)
        category = self.request.GET.get('category')
        look_for = self.request.GET.get('look_for')
        if location or category or look_for:
            if look_for == '' and category == '':
                queryset = Property.objects.filter(Q(city__icontains = location))
            elif look_for == '':
                queryset = Property.objects.filter(Q(city__icontains = location) & Q(category__slug = category))
            elif category == '':
                queryset = Property.objects.filter(Q(city__icontains = location) & Q(property_status = look_for))
            else:
                queryset = Property.objects.filter(Q(city__icontains = location) & Q(category__slug = category) & Q(property_status = look_for))
        else:
            queryset = Property.objects.all()
        return queryset
    
    def paginate_queryset(self, queryset, page_size):
        try:
            return super().paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super().paginate_queryset(queryset, page_size)