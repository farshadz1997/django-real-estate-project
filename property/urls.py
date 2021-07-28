from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home_Page, name = "Home-Page"),
    path("properties-list", views.PropertiesList.as_view(), name = "Properties-List")
]