from django.forms import ModelForm
from django import forms
from .models import *


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "followers"]
        labels = {"realname": "Name"}
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control  label-sr-only"}),
            "realname": forms.TextInput(
                attrs={"class": "form-control label-floatingTextarea"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }
