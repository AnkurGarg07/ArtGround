from django import forms
from .models import shippingInfo


class shippingForm(forms.ModelForm):
    class Meta:
        model = shippingInfo
        fields = ['first_name', 'last_name', 'email', 'phoneNumber', 'address1', 'address2', 'Country', 'State', 'City', 'zipCode', 'paymentType']
        widgets = {
            'paymentType': forms.RadioSelect,
        }
