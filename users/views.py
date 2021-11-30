from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CreatePropertyForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from property.models import Property
from django.views.generic import UpdateView, DeleteView


FIELDS = ['title', 'property_status', 'address', 'state', 'city', 'description', 'category', 'price',
              'bedrooms', 'bathrooms', 'garage', 'sqft', 'MainPhoto', 'photo_1', 'photo_2', 'photo_3',
              'photo_4', 'photo_5', 'photo_6']
  
def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(profile, args=[request.user.username]))
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

def sign_in(request): # after login it goes to profile page through sign-in view for passing username.
    return HttpResponseRedirect(reverse(profile, args=[request.user.username]))

@login_required()
def profile(request, username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect(reverse(profile, args=[request.user.username]))
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse(profile, args=[request.user.username]))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required()
def PropertyCreateView(request):
    if request.method == 'POST':
        author = Property(author = request.user)
        form = CreatePropertyForm(request.POST, request.FILES, instance = author)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your property has been listed.')
            return HttpResponseRedirect(reverse(profile, args=[request.user.username]))
    else:
        form = CreatePropertyForm()
    context = {'form': form}
    return render(request, 'users/property-create-update.html', context)

class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    template_name = 'users/property-create-update.html'
    fields = FIELDS

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Your property has been updated successfully.')
        return super().form_valid(form)

    def test_func(self):
        property = self.get_object()
        if self.request.user == property.author:
            return True
        return False

class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    template_name = 'users/property-delete.html'

    def test_func(self):
        property = self.get_object()
        if self.request.user == property.author:
            return True
        return False
    
    def get_success_url(self):
        messages.success(self.request, f'Your property has been deleted successfully.')
        return reverse(profile, args=[self.request.user.username])