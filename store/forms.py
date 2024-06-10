from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "1 246 123 4567"}
        ),
        required=False,
    )
    address = forms.CharField(
        max_length=255,
        label="Address",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "1234 Main St, City, Country",
            }
        ),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ["phone", "address"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs["class"] = "form-control"
        self.fields["address"].widget.attrs["class"] = "form-control"
