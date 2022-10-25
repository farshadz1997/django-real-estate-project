from django.shortcuts import redirect, get_list_or_404
from .models import Blog
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Q


class BlogList(ListView):
    queryset = Blog.objects.all().select_related("author").prefetch_related("comments")
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"
    ordering = "-pub_date"
    paginate_by = 6


class BlogDetail(DetailView, FormMixin):
    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"
    form_class = CommentForm
    success_url = "/"

    def get_context_data(self, *args, **kwargs):
        context = super(BlogDetail, self).get_context_data(*args, **kwargs)
        context["related_posts"] = (
            Blog.objects.filter(category=self.object.category)
            .select_related("author")
            .prefetch_related("comments")
            .exclude(id=self.object.pk)[:2]
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        self.object = self.get_object()
        new_comment.blog = self.object
        form.save()
        return redirect(self.object.get_absolute_url())

    def get_object(self, queryset=None):
        return Blog.objects.filter(pk=self.kwargs.get("pk")).select_related("author").prefetch_related("comments").first()


class BlogSearch(ListView):
    queryset = Blog.objects.all().select_related("author").prefetch_related("comments")
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"
    ordering = "-pub_date"
    paginate_by = 6

    def get_queryset(self):
        search_for = self.request.GET.get("q")
        if search_for:
            return self.queryset.filter(Q(title__icontains=search_for) | Q(content__icontains=search_for))
        return self.queryset


class CategoryView(ListView):
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"
    paginate_by = 6

    def get_queryset(self):
        return get_list_or_404(Blog.objects.select_related("author").prefetch_related("comments"), category__slug=self.kwargs["category"])


class TagView(ListView):
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"
    paginate_by = 6

    def get_queryset(self):
        return get_list_or_404(Blog.objects.select_related("author").prefetch_related("comments"), tag__slug=self.kwargs["tag"])
