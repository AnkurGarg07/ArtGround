from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer, Seller, User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'full_name']


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['phone_number', 'full_name']


class CustomLoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
