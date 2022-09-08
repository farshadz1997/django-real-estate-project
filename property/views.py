from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Property
from blog.models import Blog
from django.db.models import Max, Min
from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from .forms import SearchForm


class HomePageView(TemplateView, FormMixin):
    template_name = "property/index.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["properties"] = Property.objects.all().order_by("-pub_date")[:6]
        context["exclusive_properties"] = Property.objects.filter(status="Exc")
        context["blogs"] = Blog.objects.all().order_by("-pub_date")[:3]
        context["max_and_min"] = Property.objects.aggregate(
            minimum_price=Min("price"), maximum_price=Max("price"), minimum_sqft=Min("sqft"), maximum_sqft=Max("sqft")
        )
        return context


class PropertiesList(ListView, FormMixin):
    model = Property
    template_name = "property/properties-list.html"
    context_object_name = "properties"
    paginate_by = 6
    form_class = SearchForm

    def get_context_data(self, *args, **kwargs):
        context = super(PropertiesList, self).get_context_data(*args, **kwargs)
        context["popular_properties"] = Property.objects.order_by("-views")[:3]
        context["max_and_min"] = Property.objects.aggregate(
            minimum_price=Min("price"), maximum_price=Max("price"), minimum_sqft=Min("sqft"), maximum_sqft=Max("sqft")
        )
        get_copy = self.request.GET.copy()
        context["parameters"] = get_copy.pop("page", True) and get_copy.urlencode()
        return context

    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_ordering(self):
        if self.request.GET.get("sort_by") == "Name":
            return "-title"
        elif self.request.GET.get("sort_by") == "Price":
            return "-price"
        elif self.request.GET.get("sort_by") == "Date":
            return "-pub_date"
        else:
            return self.ordering

    def get_initial(self):
        return {"sort_by": self.request.GET.get("sort_by", "Date"), "paginate_by": self.request.GET.get("paginate_by", "6")}


class PropertyDetailView(DetailView, FormMixin):
    model = Property
    template_name = "property/properties-detail.html"
    context_object_name = "property"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nearby_properties"] = Property.objects.order_by("?").filter(city=self.object.city).exclude(id=self.object.pk)[:2]
        context["popular_properties"] = Property.objects.order_by("-views").exclude(id=self.object.pk)[:3]
        context["max_and_min"] = Property.objects.aggregate(
            minimum_price=Min("price"), maximum_price=Max("price"), minimum_sqft=Min("sqft"), maximum_sqft=Max("sqft")
        )
        return context

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


class UserPropertiesListView(ListView, FormMixin):
    template_name = "property/properties-list.html"
    context_object_name = "properties"
    paginate_by = 6
    form_class = SearchForm
    extra_context = {
        "max_and_min": Property.objects.aggregate(
            minimum_price=Min("price"), maximum_price=Max("price"), minimum_sqft=Min("sqft"), maximum_sqft=Max("sqft")
        )
    }

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Property.objects.filter(author=user).order_by("-pub_date")


class SearchView(ListView, FormMixin):
    template_name = "property/properties-list.html"
    context_object_name = "properties"
    paginate_by = 6
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_properties"] = Property.objects.order_by("-views")[:3]
        context["max_and_min"] = Property.objects.aggregate(
            minimum_price=Min("price"), maximum_price=Max("price"), minimum_sqft=Min("sqft"), maximum_sqft=Max("sqft")
        )
        get_copy = self.request.GET.copy()
        context["parameters"] = get_copy.pop("page", True) and get_copy.urlencode()
        return context

    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_ordering(self):
        if self.request.GET.get("sort_by") == "Name":
            return "-title"
        elif self.request.GET.get("sort_by") == "Price":
            return "-price"
        elif self.request.GET.get("sort_by") == "Date":
            return "-pub_date"
        else:
            return self.ordering

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
            "sort_by": self.request.GET.get("sort_by", "Date"),
            "paginate_by": self.request.GET.get("paginate_by", "6"),
        }
