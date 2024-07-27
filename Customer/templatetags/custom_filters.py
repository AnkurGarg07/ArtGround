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


@register.filter(name="cart_total")
def cart_total(cart):
    return sum(cart.values())


@register.filter(name='product_total')
def price_total(product, cart):
    return product.price * cart_quantity(product, cart)


@register.filter(name="get_cart_total")
def get_cart_total(products, cart):
    sum = 0
    for product in products:
        sum += price_total(product, cart)
    return sum


@register.filter(name='get_tax')
def get_tax(products, cart):
    total_price = get_cart_total(products, cart)
    total_price = float(total_price)
    tax = (5.0 / 100) * total_price
    return round(tax, 2)


@register.filter(name='get_total')
def get_total_price(products, cart):
    cart_total = float(get_cart_total(products, cart))
    tax = get_tax(products, cart)
    total_price = cart_total + tax + 60.0
    return total_price
