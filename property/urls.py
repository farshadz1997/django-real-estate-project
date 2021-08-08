from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home_Page, name = "Home-Page"),
    path("properties-list", views.PropertiesList.as_view(), name = "Properties-List"),
    path("properties-detail/<int:pk>", views.PropertyDetailView.as_view(), name = "Properties-Detail"),
    path("search", views.SearchView.as_view(), name = "Search"),
    path("gallery", views.GalleryView.as_view(), name = "Gallery"),
]