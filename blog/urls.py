from django.urls import path
from . import views
from .api import viewsets as api_viewsets

app_name = "blog"

blog_list = api_viewsets.BlogAPI.as_view({"get": "list"})
blog_detail = api_viewsets.BlogAPI.as_view({"get": "retrieve", "post": "create"})

urlpatterns = [
    path("blogs", views.BlogList.as_view(), name="Blogs-List"),
    path("blogs/<int:pk>", views.BlogDetail.as_view(), name="Blog-Detail"),
    path("blogs/search", views.BlogSearch.as_view(), name="Blog-Search"),
    path(
        "blogs/categories/<slug:category>/",
        views.CategoryView.as_view(),
        name="Blog-Category",
    ),
    path("blogs/tags/<slug:tag>/", views.TagView.as_view(), name="Blog-Tag"),
    ######## API ########
    path("api/blogs/", blog_list, name="api_blog_list"),
    path("api/blogs/<int:pk>/", blog_detail, name="api_blog_detail"),
    path("api/blogs/search/", api_viewsets.BlogSearchAPI.as_view(), name="api_blog_search"),
    path("api/blogs/categories/", api_viewsets.CategoryAPI.as_view(), name="api_categories"),
    path("api/blogs/categories/<slug:category>/", api_viewsets.BlogsByCategoryAPI.as_view(), name="api_blog_category"),
    path("api/blogs/tags/", api_viewsets.TagAPI.as_view(), name="api_tags"),
    path("api/blogs/tags/<slug:tag>/", api_viewsets.BlogsByTagAPI.as_view(), name="api_blog_tag"),
]
