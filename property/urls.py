from django.urls import path
from . import views

app_name = "property"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="Home-Page"),
    path("properties/", views.PropertiesList.as_view(), name="Properties-List"),
    path("properties/<int:pk>/", views.PropertyDetailView.as_view(), name="Properties-Detail"),
    path("properties/users/<str:username>/", views.UserPropertiesListView.as_view(), name="user-properties"),
    path("properties/search/", views.SearchView.as_view(), name="Search"),
]
