from multiprocessing import AuthenticationError
from rest_framework import serializers
from ..models import Blog, Category, Tag, Comments

from django.db.models import Count


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        exclude = ("blog",)
        
    def create(self, validated_data):
        blog = Blog.objects.get(id=self.context["request"].data.get("blog"))
        comment = Comments.objects.create(blog=blog, **validated_data)
        return comment


class BlogListSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return obj.author.username
    
    def get_category(self, obj):
        return obj.category.title
    
    class Meta:
        model = Blog
        extra_kwargs = {"url": {"view_name": "blog:api_blog_detail", "lookup_field": "pk"}}
        exclude = ("tag",)
        
        
class BlogDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.title
    
    def get_tags(self, obj):
        return obj.tag.all().values_list("title", flat=True)
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_author(self, obj):
        return obj.author.username
    
    class Meta:
        model = Blog
        exclude = ("tag", "slug")