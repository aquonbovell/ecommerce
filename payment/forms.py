from django import forms

from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(attrs={"placeholder": "Full Name"}),
        required=True,
    )
    shipping_email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
        required=True,
    )
    shipping_address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs={"placeholder": "Address"}),
        required=True,
    )
    shipping_city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={"placeholder": "City"}),
        required=True,
    )
    shipping_postal_code = forms.CharField(
        label="Postal Code",
        widget=forms.TextInput(attrs={"placeholder": "Postal Code"}),
        required=True,
    )

    class Meta:
        model = ShippingAddress
        fields = [
            "shipping_full_name",
            "shipping_email",
            "shipping_address",
            "shipping_city",
            "shipping_postal_code",
        ]
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label="Card Number",
        widget=forms.TextInput(attrs={"placeholder": "Card Number"}),
        required=True,
    )
    card_expiry = forms.CharField(
        label="Card Expiry",
        widget=forms.TextInput(attrs={"placeholder": "MM/YY"}),
        required=True,
    )
    card_cvv = forms.CharField(
        label="Card CVV",
        widget=forms.TextInput(attrs={"placeholder": "CVV"}),
        required=True,
    )
    card_name = forms.CharField(
        label="Card Name",
        widget=forms.TextInput(attrs={"placeholder": "Card Name"}),
        required=True,
    )
    card_address1 = forms.CharField(
        label="Card Address1",
        widget=forms.TextInput(attrs={"placeholder": "Card Address1"}),
        required=True,
    )
    card_address2 = forms.CharField(
        label="Card Address2",
        widget=forms.TextInput(attrs={"placeholder": "Card Address2"}),
        required=True,
    )
    card_city = forms.CharField(
        label="Card City",
        widget=forms.TextInput(attrs={"placeholder": "Card City"}),
        required=True,
    )
    card_state = forms.CharField(
        label="Card State",
        widget=forms.TextInput(attrs={"placeholder": "Card State"}),
        required=True,
    )
    card_postal_code = forms.CharField(
        label="Card Postal Code",
        widget=forms.TextInput(attrs={"placeholder": "Card Postal Code"}),
        required=True,
    )
    card_country = forms.CharField(
        label="Card Country",
        widget=forms.TextInput(attrs={"placeholder": "Card Country"}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
