from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "slug", "pub_date", "update_date", "category")
    list_display_links = ("title",)
    list_filter = ("category", "author")
    search_fields = ("title", "content")
    date_hierarchy = "pub_date"


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "pub_date")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "pub_date")


@admin.register(models.Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog", "email", "date")
    search_fields = ("name", "email", "comment")
    list_per_page = 10
