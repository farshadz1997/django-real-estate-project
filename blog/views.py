from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Blog, Category, Comments, Tag
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q

class BlogList(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    ordering = '-pub_date'
    paginate_by = 6
    
    def get_context_data(self, *args, **kwargs):
        context = super(BlogList, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(num_blogs=Count('blog'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.order_by('-pub_date')[:3]
        return context
    
class BlogDetail(FormMixin,DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    form_class = CommentForm
    
    def get_context_data(self, *args, **kwargs):
        context = super(BlogDetail, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(num_blogs=Count('blog'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.order_by('-pub_date').exclude(id=self.object.pk)[:3]
        context['related_posts'] = Blog.objects.all().filter(category = self.object.category).exclude(id=self.object.pk)[:2]
        context['comments'] = Comments.objects.all().filter(blog = self.object)
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            self.object = self.get_object()
            new_comment.blog = self.object
            context = super(BlogDetail, self).get_context_data(*args, **kwargs)
            context = self.get_context_data(*args, **kwargs)
            context['form'] = CommentForm()
            form.save()
            return HttpResponseRedirect(reverse("Blog-Detail", kwargs={"pk":self.object.pk}))
        else:
            context = super(BlogDetail, self).get_context_data(*args, **kwargs)
            context = self.get_context_data(*args, **kwargs)
            context['form'] = CommentForm()
            return self.render_to_response(context=context)
        
class BlogSearch(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    ordering = '-pub_date'
    paginate_by = 6
    
    def get_context_data(self, *args, **kwargs):
        context = super(BlogSearch, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(num_blogs=Count('blog'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.order_by('-pub_date')[:3]
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        return context
      
    def get_queryset(self):
        search_for = self.request.GET.get('q')
        if search_for:
            query = Blog.objects.filter(Q(title__icontains=search_for) | Q(content__icontains=search_for))
        else:
            query = Blog.objects.all()
        return query
    
class CategoryView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().annotate(num_blogs=Count('blog'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.order_by('-pub_date')[:3]
        return context
    
    def get_queryset(self):
        return Blog.objects.filter(category__slug = self.kwargs['category'])

class TagView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().annotate(num_blogs=Count('blog'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.order_by('-pub_date')[:3]
        return context
    
    def get_queryset(self):
        return Blog.objects.filter(tag__slug = self.kwargs['tag'])