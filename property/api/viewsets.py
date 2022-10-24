from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import resolve
from django.db.models import Q, Min, Max

from ..models import Property, Category
from .serializers import PropertyListSerializer, CategorySerializer, PropertyDetailSerializer


class PropertyAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all()

    def get_serializer_class(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name == "api_property_detail":
            return PropertyDetailSerializer
        return PropertyListSerializer
    
    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context["request"] = self.request
        return context
    

class SearchAPI(generics.ListAPIView):
    serializer_class = PropertyListSerializer
    queryset = Property.objects.all()

    def filter_queryset(self, queryset):
        request = self.request.GET
        property_overview = queryset.aggregate(min_sqft=Min("sqft"), max_sqft=Max("sqft"), min_price=Min("price"), max_price=Max("price"))
        if request.get("location"):
            queryset = queryset.filter(Q(city__icontains=request.get("location")))
        if request.get("category"):
            queryset = queryset.filter(Q(category=request.get("category")))
        if request.get("look_for"):
            queryset = queryset.filter(Q(property_status=request.get("look_for")))
        if request.get("min_sqft") or request.get("max_sqft"):
            queryset = queryset.filter(
                Q(
                    sqft__range=(
                        request.get("min_sqft", property_overview["min_sqft"]),
                        request.get("max_sqft", property_overview["max_sqft"]),
                    )
                )
            )
        if request.get("min_price") or request.get("max_price"):
            queryset = queryset.filter(
                Q(
                    price__range=(
                        request.get("min_price", property_overview["min_price"]),
                        request.get("max_price", property_overview["max_price"]),
                    )
                )
            )
        return queryset


class SearchFormDataAPI(APIView):
    def get(self, request):
        data = Property.objects.aggregate(min_sqft=Min("sqft"), max_sqft=Max("sqft"), min_price=Min("price"), max_price=Max("price"))
        data["property_choices"] = dict(Property.property_choices)
        data["category"] = CategorySerializer(Category.objects.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)