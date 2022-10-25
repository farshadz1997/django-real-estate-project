from django.db.models import Count

from .models import Blog, Category, Tag

def blog_context(request):
    categories = Category.objects.all().annotate(num_blogs=Count("blog"))
    tags = Tag.objects.all()
    recent_posts = Blog.objects.order_by("-pub_date")[:3]
    return {"categories": categories, "tags": tags, "recent_posts": recent_posts}