from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormCore
from .models import Profile
from property.models import Property
from .tasks import send_create_property_email_task, send_password_reset_email_task


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
    
    def send_email(self, email: str):
        return send_create_property_email_task.delay(
            self.cleaned_data["title"],
            self.instance.get_property_status_display(),
            self.cleaned_data["description"],
            [email])

    class Meta:
        model = Property
        exclude = ["author", "views", "status"]


class PasswordResetForm(PasswordResetFormCore):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={"autocomplete": "email"}
    ))

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        This method is inherating Django's core `send_mail` method from `PasswordResetForm` class
        """
        context['user'] = context['user'].id
        send_password_reset_email_task.delay(
            subject_template_name=subject_template_name, 
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name
        )