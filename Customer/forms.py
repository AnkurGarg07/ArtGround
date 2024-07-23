from django import forms
from .models import shippingInfo


class shippingForm(forms.ModelForm):
    class Meta:
        model = shippingInfo
        fields = '__all__'
        widgets = {
            'paymentType': forms.RadioSelect,
        }
