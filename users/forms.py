from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
from property.models import Property


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


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


class CreatePropertyForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "1234 Main St"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"style": "resize:none;"}))
    state = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "e.g Califronia"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "e.g Los Angles"}))

    class Meta:
        model = Property
        exclude = ["author", "views", "status"]
