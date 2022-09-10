from django import forms
from .models import Category


class SearchForm(forms.Form):
    location = forms.CharField(
        max_length=20,
        min_length=3,
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={"placeholder": "Type your location", "type": "text"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(),
        required=False,
        empty_label="Category",
    )
    look_for = forms.ChoiceField(
        choices=[
            (None, "Look for"),
            ("FS", "For Sale"),
            ("FR", "For Rent"),
            ("SL", "Sold Out"),
        ],
        required=False,
    )
    # sqft slider
    min_sqft = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={"type": "hidden", "id": "min_sqft"}))
    max_sqft = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={"type": "hidden", "id": "max_sqft"}))
    # price slider
    min_price = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={"type": "hidden", "id": "min_price"}))
    max_price = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={"type": "hidden", "id": "max_price"}))

    sort_by = forms.ChoiceField(
        choices=[("pub_date", "Date"), ("title", "Name"), ("price", "Price")],
        required=False,
        widget=forms.Select(),
    )
    paginate_by = forms.ChoiceField(
        choices=[("6", "6"), ("12", "12"), ("18", "18"), ("24", "24")],
        required=False,
        widget=forms.Select(),
    )
