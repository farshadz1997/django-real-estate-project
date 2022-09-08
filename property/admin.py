from django.contrib import admin
from .models import Property, Category


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "category",
        "property_status",
        "status",
        "pub_date",
        "update_date",
    )
    list_display_links = ("id", "title")
    list_filter = ("category", "property_status", "status")
    list_editable = ("status",)
    search_fields = ("title", "description")
    date_hierarchy = "pub_date"
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    list_display_links = ("title", "slug")
