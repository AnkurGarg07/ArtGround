from itertools import product

from django import forms
from .models import Product

class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=['name','price','category','description','image','size']
