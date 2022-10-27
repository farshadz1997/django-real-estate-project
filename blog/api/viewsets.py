from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView

from django.db.models import Q
from django.utils import timezone

from ..models import Blog, Category, Tag

from .serializers import BlogListSerializer, BlogDetailSerializer, CategorySerializer, CommentSerializer, TagSerializer


class BlogAPI(viewsets.ModelViewSet):
    queryset = Blog.objects.all().select_related("author").prefetch_related("comments")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogDetailSerializer
        return BlogListSerializer

    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        data = request.data
        obj = self.get_object()
        data["date"] = timezone.now()
        data["blog_id"] = obj.id
        serializer = CommentSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {"request": self.request}


class CategoryAPI(APIView):
    def get(self, request, *args, **kwargs):
        query = Category.objects.all()
        serializer = CategorySerializer(query, many=True, context={"request": request})
        return Response(serializer.data)


class BlogsByCategoryAPI(APIView):
    def get(self, request, *args, **kwargs):
        query = Blog.objects.filter(category__slug=self.kwargs["category"]).select_related("author").prefetch_related("comments")
        serializer = BlogListSerializer(query, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagAPI(APIView):
    def get(self, request, *args, **kwargs):
        query = Tag.objects.all()
        serializer = TagSerializer(query, many=True, context={"request": request})
        return Response(serializer.data)


class BlogsByTagAPI(APIView):
    def get(self, request, *args, **kwargs):
        query = Blog.objects.filter(tag__slug=self.kwargs["tag"]).select_related("author").prefetch_related("comments")
        serializer = BlogListSerializer(query, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogSearchAPI(generics.ListAPIView):
    queryset = Blog.objects.all().select_related("author").prefetch_related("comments")
    serializer_class = BlogListSerializer

    def filter_queryset(self, queryset):
        request = self.request.GET
        if request.get("q"):
            queryset = queryset.filter(Q(title__icontains=request.get("q")) | Q(content__icontains=request.get("q")))
        return queryset
