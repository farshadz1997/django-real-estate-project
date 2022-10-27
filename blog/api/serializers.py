from rest_framework import serializers
from ..models import Blog, Category, Tag, Comments


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d %b %Y %H:%M")

    class Meta:
        model = Comments
        exclude = ("blog", "id")

    def create(self, validated_data):
        comment = Comments.objects.create(blog_id=self.initial_data["blog_id"], **validated_data)
        return comment


class BlogListSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.CharField(source="category.title")
    author = serializers.CharField(source="author.username")
    comments_count = serializers.SerializerMethodField()
    pub_date = serializers.DateTimeField(format="%d %b %Y %H:%M")
    update_date = serializers.DateTimeField(format="%d %b %Y %H:%M")

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Blog
        extra_kwargs = {"url": {"view_name": "blog:api_blog_detail", "lookup_field": "pk"}}
        exclude = ("tag", "slug")


class BlogDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    category = serializers.CharField(source="category.title")
    tags = serializers.SerializerMethodField()
    author = serializers.CharField(source="author.username")
    pub_date = serializers.DateTimeField(format="%d %b %Y %H:%M")
    update_date = serializers.DateTimeField(format="%d %b %Y %H:%M")

    def get_tags(self, obj):
        return obj.tag.all().values_list("title", flat=True)

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Blog
        exclude = ("tag", "slug")


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        extra_kwargs = {"url": {"view_name": "blog:api_blog_category", "lookup_field": "slug", "lookup_url_kwarg": "category"}}
        fields = ("title", "url")


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ("title", "url")
        extra_kwargs = {"url": {"view_name": "blog:api_blog_tag", "lookup_field": "slug", "lookup_url_kwarg": "tag"}}
