from django import template

from Seller.models import Product

register = template.Library()


@register.filter(name='total_products_listed')
def total_products_list(user):
    products = list(Product.objects.filter(seller=user))
    return len(products)


@register.filter(name='total_products_sold')
def total_products_sold(product_sales):
    return sum(product.quantity for product in product_sales)


@register.filter(name='total_revenue_generated')
def total_revenue_generated(product_sales):
    return sum(product.price for product in product_sales)