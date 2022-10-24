from django.urls import path
from . import views
from .api import viewsets as api_views

app_name = "property"

propery_list = api_views.PropertyAPI.as_view({"get": "list"})
propery_detail = api_views.PropertyAPI.as_view({"get": "retrieve"})

urlpatterns = [
    path("", views.HomePageView.as_view(), name="Home-Page"),
    path("properties/", views.PropertiesList.as_view(), name="Properties-List"),
    path("properties/<int:pk>/", views.PropertyDetailView.as_view(), name="Properties-Detail"),
    path("properties/users/<str:username>/", views.UserPropertiesListView.as_view(), name="user-properties"),
    path("properties/search/", views.SearchView.as_view(), name="Search"),
    ######## API ########
    path("api/properties/", propery_list, name="api_property_list"),
    path("api/properties/<int:pk>/", propery_detail, name="api_property_detail"),
    path("api/search/", api_views.SearchAPI.as_view(), name="api_search_property"),
    path("api/search-form-data/", api_views.SearchFormDataAPI.as_view(), name="api_search_form_data"),
]
