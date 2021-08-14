from django.urls import path
from . import views

urlpatterns = [
    path("blogs", views.BlogList.as_view(), name="Blogs-List"),
    path("blogs/<int:pk>", views.BlogDetail.as_view(), name="Blog-Detail"),
    path("blogs/search", views.BlogList.as_view(), name="Blog-Search"),
]