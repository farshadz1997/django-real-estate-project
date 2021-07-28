from django.db import models
from django.utils import timezone

class Property(models.Model):
    property_choices = [
        ('FS', 'For Sale'),
        ('FR', 'For Rent'),
        ('SL', 'Sold Out')
    ]
    title = models.CharField(max_length=255)
    property_status = models.CharField(max_length = 2, choices = property_choices)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits = 2, decimal_places = 1)
    garage = models.IntegerField(default = 0)
    sqft = models.IntegerField(verbose_name = "Area", blank = False, null = False)
    MainPhoto = models.ImageField(upload_to = "Properties/")
    photo_1 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_2 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_3 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_4 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_5 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    photo_6 = models.ImageField(upload_to = "Properties/", blank = True, null = True)
    pub_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True, auto_now_add = False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    