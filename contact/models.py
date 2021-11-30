from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    subject = models.CharField(max_length=255, null=False, blank=False)
    message = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.email