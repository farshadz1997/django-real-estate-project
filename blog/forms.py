from django import forms
from .models import Comments

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'style':'resize:none;'}))
    class Meta:
        model = Comments
        fields = ('name', 'email', 'comment')