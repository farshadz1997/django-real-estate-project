from django.db import models
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse

class Blog(models.Model):
    title = models.CharField(max_length=55, verbose_name='Title')
    author = models.ForeignKey(User, verbose_name='Author', on_delete = models.CASCADE, blank=False, null=False)
    category = models.ForeignKey("Category", related_name="blog", verbose_name='Category', on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ManyToManyField("Tag", related_name="blogs", verbose_name='Tags', blank=True)
    image = models.ImageField(upload_to='blogs/', verbose_name='Image')
    content = RichTextField()
    slug = AutoSlugField(populate_from='title')
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:Blog-Detail', kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ('-pub_date',)
    
class Category(models.Model):
    title = models.CharField(max_length=55, verbose_name='Title')
    slug = AutoSlugField(populate_from='title')
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:Blog-Category", kwargs={"category": self.slug})
    
    class Meta:
        verbose_name_plural = "Catrgories"
        
        
class Tag(models.Model):
    title = models.CharField(max_length=55, verbose_name='Title')
    slug = AutoSlugField(populate_from='title')
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:Blog-Tag", kwargs={"tag": self.slug})
    
    
class Comments(models.Model):
    blog = models.ForeignKey("Blog", verbose_name="Blog", on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=55, verbose_name="Name")
    email = models.EmailField(max_length=100, verbose_name="Email")
    comment = models.TextField(verbose_name="Comment")
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"