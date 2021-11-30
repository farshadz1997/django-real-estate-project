from django.contrib import admin
from .models import Contact
# Register your models here.
# admin.site.register(Contact)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'date')
    list_display_links = ('name', 'email')
    search_fields = ('name', 'email', 'subject', 'message')
    list_per_page = 25