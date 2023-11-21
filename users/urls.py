from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import PasswordResetForm


app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name = "login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/<str:username>', views.profile, name='profile'),
    path("property/new/", views.PropertyCreateView.as_view(), name = "create-property"),
    path("change-password/", views.ChangePasswordView.as_view(), name = "change-password"),
    path('post/<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property-update'),
    path("property/<int:pk>/update/", views.PropertyUpdateView.as_view(), name = "update-property"),
    path("property/<int:pk>/delete/", views.PropertyDeleteView.as_view(), name = "delete-property"),
    # password reset
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        form_class=PasswordResetForm,
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')),
        name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy("users:password_reset_complete")),
        name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]