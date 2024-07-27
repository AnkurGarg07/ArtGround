from django import template

from Seller.models import Product

register = template.Library()


@register.filter(name='total_products_listed')
def total_products_list(user):
    products = list(Product.objects.filter(seller=user))
    return len(products)
