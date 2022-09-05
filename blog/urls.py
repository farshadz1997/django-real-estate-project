from django.urls import path
from . import views

app_name = "blog"

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
]
