from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from . import models
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Count

class BlogList(ListView):
    model = models.Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-pub_date']
    paginate_by = 8
    
    def get_context_data(self, *args, **kwargs):
        context = super(BlogList, self).get_context_data(*args, **kwargs)
        context['categories'] = models.Category.objects.all().annotate(num_blogs=Count('blog'))
        context['tags'] = models.Tag.objects.all()
        context['recent_posts'] = models.Blog.objects.order_by('-pub_date')[:3]
        return context
    
    def get_queryset(self):
        search_for = self.request.GET.get('search_for')
        if search_for:
            query_set = models.Blog.objects.filter(title__icontains = search_for, description__icontains = search_for, content__icontains = search_for)
        else:
            query_set = models.Blog.objects.all()
        return query_set
    
class BlogDetail(FormMixin,DetailView):
    model = models.Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    form_class = CommentForm
    
    def get_context_data(self, *args, **kwargs):
        context = super(BlogDetail, self).get_context_data(*args, **kwargs)
        context['categories'] = models.Category.objects.all().annotate(num_blogs=Count('blog'))
        context['tags'] = models.Tag.objects.all()
        context['recent_posts'] = models.Blog.objects.order_by('-pub_date').exclude(id=self.object.pk)[:3]
        context['related_posts'] = models.Blog.objects.all().filter(category = self.object.category).exclude(id=self.object.pk)[:2]
        context['comments'] = models.Comments.objects.all().filter(blog = self.object)
        context['form'] = CommentForm()
        return context
    
    def get_queryset(self):
        search_for = self.request.GET.get('search_for')
        if search_for:
            query_set = models.Blog.objects.filter(title__icontains = search_for, description__icontains = search_for, content__icontains = search_for)
        else:
            query_set = models.Blog.objects.all()
        return query_set
    
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