from django import template

register = template.Library()


@register.filter(name="is_in_cart")
def is_in_cart(item, cart):
    all_products = cart.keys()
    for id in all_products:
        if id == item.product_id:
            return True
    return False


@register.filter(name="cart_quantity")
def cart_quantity(item, cart):
    all_products = cart.keys()
    for id in all_products:
        if id == item.product_id:
            return cart.get(id)
    return 0
