from django.db import models

from Account.models import Customer
from Seller.models import Order


# Create your models here.
class shippingInfo(models.Model):
    choices = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('UPI', 'UPI')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,default=None)
    order=models.ForeignKey(Order, on_delete=models.CASCADE,default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=10)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,blank=True, null=True)
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    zipCode = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=50, choices=choices, default='Bank Transfer')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
