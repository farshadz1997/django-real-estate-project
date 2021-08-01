from django.db import models
from django.utils import timezone
from django.urls import reverse

class Property(models.Model):
    property_choices = [
        ('FS', 'For Sale'),
        ('FR', 'For Rent'),
        ('SL', 'Sold Out')
    ]
    title = models.CharField(max_length=255, verbose_name = "Title", help_text = "Title of the property")
    property_status = models.CharField(max_length = 2, choices = property_choices, verbose_name = "Property status")
    address = models.CharField(max_length=255, verbose_name = "Address")
    state = models.CharField(max_length=255, verbose_name = "State")
    city = models.CharField(max_length=255, verbose_name = "City")
    description = models.TextField(blank = True, verbose_name = 'Description')
    category = models.ForeignKey("Category", related_name = "property", verbose_name = "Category", on_delete = models.CASCADE, blank = True, null=True)
    price = models.IntegerField(verbose_name = 'Price')
    bedrooms = models.IntegerField(verbose_name = 'Bedrooms')
    bathrooms = models.DecimalField(max_digits = 2, decimal_places = 1, verbose_name = 'Bathrooms')
    garage = models.IntegerField(default = 0, verbose_name = 'Garage')
    sqft = models.IntegerField(verbose_name = "Area")
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
        return reverse('Properties-Detail', kwargs={'pk': self.pk})
    
class Category(models.Model):
    title = models.CharField(verbose_name = "Title", max_length = 50)
    slug = models.SlugField(verbose_name = "Slug")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.title 
    