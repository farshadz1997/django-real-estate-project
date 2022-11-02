from django.urls import path
from . import viewsets as api_viewsets

app_name = "api_property"

property_list = api_viewsets.PropertyAPI.as_view({"get": "list"})
property_detail = api_viewsets.PropertyAPI.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})

urlpatterns = [
    path("api/properties/", property_list, name="api_property_list"),
    path("api/properties/<int:pk>/", property_detail, name="api_property_detail"),
    path("api/search/", api_viewsets.SearchAPI.as_view(), name="api_search_property"),
    path("api/search-form-data/", api_viewsets.SearchFormDataAPI.as_view(), name="api_search_form_data"),
    path("api/user-properties/<str:username>/", api_viewsets.UserPropertyListAPI.as_view(), name="api_user_property"),
    path("api/properties/create/", api_viewsets.CreatePropertyAPI.as_view(), name="api_create_property"),
    
]