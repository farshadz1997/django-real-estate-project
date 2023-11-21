from rest_framework import status, viewsets, generics, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from django.db.models import Q, Min, Max

from ..models import Property, Category
from .serializers import PropertyListSerializer, CategorySerializer, PropertyDetailSerializer


class PropertyAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Property.objects.all().select_related("category", "author")

    def check_object_permissions(self, request, obj):
        if request.method == "PUT" or request.method == "DELETE":
            if obj.author != request.user:
                self.permission_denied(request, message="You are not allowed to access this property", code=403)
        super().check_object_permissions(request, obj)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PropertyDetailSerializer
        return PropertyListSerializer

    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PropertyDetailSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, **serializer.validated_data)
        return Response(serializer.data)


class UserPropertyListAPI(generics.ListAPIView):
    serializer_class = PropertyListSerializer

    def get_queryset(self, queryset=None):
        return Property.objects.filter(author__username=self.kwargs["username"]).select_related("author", "category")

    def get_serializer_context(self):
        return {"request": self.request}


class CreatePropertyAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """category and property status to display in the form"""
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response({"categories": serializer.data, "property_status": dict(Property.property_choices)}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PropertyDetailSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.create(**serializer.validated_data)
        serializer.send_email(request.user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
