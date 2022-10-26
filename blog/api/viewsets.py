from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView

from django.urls import resolve
from django.db.models import Q

from ..models import Blog, Category, Tag, Comments

from .serializers import BlogListSerializer, BlogDetailSerializer, CommentSerializer


class BlogAPI(viewsets.ModelViewSet):
    queryset = Blog.objects.all().select_related("author").prefetch_related("comments")
    
    def get_serializer_class(self):
        if resolve(self.request.path_info).url_name == "api_blog_detail":
            return BlogDetailSerializer
        return BlogListSerializer
    
    def create(self, request):
        serializer = CommentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_context(self):
        return {"request": self.request}
    

class CategoryAPI(APIView):
    def get(self, request):
        query = Blog.objects.filter(category__slug=self.kwargs["category"]).select_related("author").prefetch_related("comments")
        serializer = BlogListSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TagAPI(APIView):
    def get(self, request):
        query = Blog.objects.filter(tags__slug=self.kwargs["tag"]).select_related("author").prefetch_related("comments")
        serializer = BlogListSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BlogSearchAPI(generics.ListAPIView):
    queryset = Blog.objects.all().select_related("author").prefetch_related("comments")
    serializer_class = BlogListSerializer
    
    def filter_queryset(self, queryset):
        request = self.request.GET
        if request.get("q"):
            queryset = queryset.filter(Q(title__icontains=request.get("q")) | Q(content__icontains=request.get("q")))
        return queryset