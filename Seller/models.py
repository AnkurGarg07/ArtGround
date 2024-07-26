from django.db import models
from nanoid import generate

from Account.models import Seller, User


# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('null', 'Select Category'),
        ('oil', 'Oil painting'),
        ('acrylic', 'Acrylic painting'),
        ('water', 'water painting'),
        ('pastel', 'pastel painting'),
        ('spray', 'spray painting'),
        ('other', 'other painting')
    ]

    SIZE_CHOICES = [
        ('null', 'Select Size'),
        ('4x8', '4 x 8 inches (10.16 x 20.32 cm) - Small'),
        ('8x10', '8 x 10 inches (20.32 x 25.4 cm) - Medium'),
        ('16x20', '16 x 20 inches (40.64 x 50.8 cm) - Large'),
        ('24x30', '24 x 30 inches (60.96 x 76.2 cm) - Large'),
    ]

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = generate(size=10)
        super().save(*args, **kwargs)

    product_id = models.CharField(primary_key=True, max_length=10, unique=True, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='null')
    size = models.CharField(max_length=6, choices=SIZE_CHOICES, default='null')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate(size=10)
        super().save(*args, **kwargs)
    order_id = models.CharField(primary_key=True, max_length=10, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}-{self.order_id}"


class OrderItem(models.Model):
    def save(self, *args, **kwargs):
        if not self.order_item_id:
            self.order_item_id = generate(size=10)
        super().save(*args, **kwargs)
    order_item_id = models.CharField(primary_key=True, max_length=10, unique=True, editable=False)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} {self.quantity} {self.price}"
