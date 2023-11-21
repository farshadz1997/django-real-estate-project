from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CreatePropertyForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from property.models import Property
from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib.auth import views as auth_views
from django.views.generic import FormView
from django.urls import reverse_lazy


FIELDS = [
    "title",
    "property_status",
    "address",
    "state",
    "city",
    "description",
    "category",
    "price",
    "bedrooms",
    "bathrooms",
    "garage",
    "sqft",
    "MainPhoto",
    "photo_1",
    "photo_2",
    "photo_3",
    "photo_4",
    "photo_5",
    "photo_6",
]


class RegisterView(SuccessMessageMixin, FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    success_message = "Your account has been created! You are now able to log in"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:profile", request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("users:profile", args=[self.request.user.username])


@login_required()
def profile(request, username):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated")
            return redirect("users:profile", request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "users/profile.html", context)


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "users/change_password.html"
    form_class = PasswordChangeForm
    success_message = "Your password has been changed!"

    def get_success_url(self):
        return reverse("users:profile", args=[self.request.user.username])


class PropertyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "users/property-create-update.html"
    form_class = CreatePropertyForm
    success_message = "Your property has been listed!"

    def form_valid(self, form: CreatePropertyForm):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.send_email(self.request.user.email)
        return response

    def get_success_url(self):
        return reverse("users:profile", args=[self.request.user.username])


class PropertyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Property
    template_name = "users/property-create-update.html"
    fields = FIELDS
    success_message = "Your property has been updated successfully."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        property = self.get_object()
        if self.request.user == property.author:
            return True
        return False


class PropertyDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Property
    template_name = "users/property-delete.html"
    success_message = "Your property has been deleted successfully."

    def test_func(self):
        property = self.get_object()
        if self.request.user == property.author:
            return True
        return False

    def get_success_url(self):
        return reverse("users:profile", args=[self.request.user.username])
