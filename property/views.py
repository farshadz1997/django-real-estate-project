from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Property
from blog.models import Blog
from django.db.models import Q, F
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from .forms import SearchForm
from django.core.paginator import Paginator, EmptyPage


class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class HomePageView(TemplateView, FormMixin):
    template_name = "property/index.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["properties"] = Property.objects.all().order_by("-pub_date")[:6]
        context["exclusive_properties"] = Property.objects.filter(status="Exc")
        context["blogs"] = Blog.objects.all().select_related("author").prefetch_related("comments").order_by("-pub_date")[:3]
        return context


class PropertiesList(ListView, FormMixin):
    model = Property
    template_name = "property/properties-list.html"
    context_object_name = "properties"
    paginate_by = 6
    paginator_class = MyPaginator
    form_class = SearchForm

    def get_context_data(self, *args, **kwargs):
        context = super(PropertiesList, self).get_context_data(*args, **kwargs)
        context["popular_properties"] = Property.objects.order_by("-views")[:3]
        return context

    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_ordering(self):
        return f"-{self.request.GET.get('sort_by', 'pub_date')}"

    def get_initial(self):
        return {"sort_by": self.request.GET.get("sort_by", "Date"), "paginate_by": self.request.GET.get("paginate_by", "6")}
    
        
class PropertyDetailView(DetailView, FormMixin):
    model = Property
    template_name = "property/properties-detail.html"
    context_object_name = "property"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nearby_properties"] = Property.objects.filter(city=self.object.city).exclude(id=self.object.pk).order_by("?")[:2]
        context["popular_properties"] = Property.objects.exclude(id=self.object.pk).order_by("-views")[:3]
        return context

    def get_object(self):
        obj = super().get_object()
        obj.views = F("views") + 1
        obj.save()
        obj.refresh_from_db()
        return obj
    

class UserPropertiesListView(ListView, FormMixin):
    template_name = "property/properties-list.html"
    context_object_name = "properties"
    paginate_by = 6
    paginator_class = MyPaginator
    form_class = SearchForm

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Property.objects.filter(author=user).order_by(f"-{self.request.GET.get('sort_by', 'pub_date')}")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_properties"] = Property.objects.order_by("-views")[:3]
        return context
    
    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)
    
    def get_ordering(self):
        return f"-{self.request.GET.get('sort_by', 'pub_date')}"
    
    def get_initial(self):
        return {"sort_by": self.request.GET.get("sort_by", "Date"), "paginate_by": self.request.GET.get("paginate_by", "6")}


class SearchView(ListView, FormMixin):
    template_name = "property/properties-list.html"
    context_object_name = "properties"
    paginate_by = 6
    paginator_class = MyPaginator    
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_properties"] = Property.objects.order_by("-views")[:3]
        return context

    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_ordering(self):
        return f"-{self.request.GET.get('sort_by', 'pub_date')}"

    def get_queryset(self):
        request = self.request.GET
        queryset = Property.objects.all()
        if request.get("location"):
            queryset = queryset.filter(Q(city__icontains=request.get("location")))
        if request.get("category"):
            queryset = queryset.filter(Q(category=request.get("category")))
        if request.get("look_for"):
            queryset = queryset.filter(Q(property_status=request.get("look_for")))
        if request.get("min_sqft") or request.get("max_sqft"):
            queryset = queryset.filter(Q(sqft__range=(request.get("min_sqft"), request.get("max_sqft"))))
        if request.get("min_price") or request.get("max_price"):
            queryset = queryset.filter(Q(price__range=(request.get("min_price"), request.get("max_price"))))
        return queryset

    def get_initial(self):
        return {
            "location": self.request.GET.get("location", None),
            "category": self.request.GET.get("category", None),
            "look_for": self.request.GET.get("look_for", None),
            "min_sqft": self.request.GET.get("min_sqft", None),
            "max_sqft": self.request.GET.get("max_sqft", None),
            "min_price": self.request.GET.get("min_price", None),
            "max_price": self.request.GET.get("max_price", None),
            "sort_by": self.request.GET.get("sort_by", "pub_date"),
            "paginate_by": self.request.GET.get("paginate_by", "6"),
        }
