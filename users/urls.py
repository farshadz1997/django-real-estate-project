from django.urls import path
from . import views

urlpatterns = [
    path("signing/", views.sign_in, name = "signing-in"), # after login it goes to profile page through sign-in view for passing username.
    path("property/new/", views.PropertyCreateView, name = "create-property"),
    path("change-password/", views.change_password, name = "change-password"),
    path('post/<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property-update'),
    path("property/<int:pk>/update/", views.PropertyUpdateView.as_view(), name = "update-property"),
    path("property/<int:pk>/delete/", views.PropertyDeleteView.as_view(), name = "delete-property"),
]