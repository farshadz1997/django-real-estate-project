from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Property(models.Model):
    property_choices = [
        ('FS', 'For Sale'),
        ('FR', 'For Rent'),
        ('SL', 'Sold Out')
    ]
    STATUS = [
        ('Nor', 'Normal'),
        ('Exc', 'Exclusive')
    ]
    status = models.CharField(max_length=3, choices=STATUS, default='Nor')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=255, verbose_name = "Title")
    property_status = models.CharField(max_length = 2, choices = property_choices, verbose_name = "Property status")
    address = models.CharField(max_length=255, verbose_name = "Address")
    state = models.CharField(max_length=255, verbose_name = "State")
    city = models.CharField(max_length=255, verbose_name = "City")
    description = models.TextField(blank = True, verbose_name = 'Description')
    category = models.ForeignKey("Category", related_name = "property", verbose_name = "Category", on_delete = models.CASCADE, blank = True, null=True)
    price = models.PositiveIntegerField(verbose_name = 'Price')
    bedrooms = models.PositiveIntegerField(verbose_name = 'Bedrooms', default = 0)
    bathrooms = models.PositiveIntegerField(verbose_name = 'Bathrooms', default = 0)
    garage = models.PositiveIntegerField(default = 0, verbose_name = 'Garage')
    sqft = models.PositiveIntegerField(verbose_name = "Area", help_text = 'in SQFT')
    MainPhoto = models.ImageField(upload_to = "Properties/")
    photo_1 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_2 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_3 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_4 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_5 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_6 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    views = models.IntegerField(default = 0)
    pub_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True, auto_now_add = False)
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('property:Properties-Detail', kwargs={'pk': self.pk})
    
class Category(models.Model):
    title = models.CharField(verbose_name = "Title", max_length = 50)
    slug = models.SlugField(verbose_name = "Slug")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.title
    
    @classmethod
    def get_categories(cls):
        """Returns all categories titles for field choices used in serializers"""
        return [(category.id, category.title) for category in cls.objects.all()]
    