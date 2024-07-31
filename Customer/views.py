from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from Customer.models import shippingInfo
from Account.decorators import customer_required
from Customer.forms import shippingForm, couponForm
from Seller.models import Product, Order, OrderItem
import random


@login_required()
@customer_required
def home(request):
    if request.method == 'POST':
        product_id = request.POST.get('productID')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {product_id: 1}
        request.session['cart'] = cart
        return redirect('home')

    #handling normal open of home page
    else:
        all_products = Product.objects.all()
        best_products_limit = min(5, len(all_products))
        best_products = Product.objects.all()[:5]
        query = request.GET.get('query')
        if query:
            all_products = Product.objects.filter(name__icontains=query)
        paginator = Paginator(all_products, 10)
        page_num = request.GET.get('page')
        if not page_num:
            page_num = 1
        all_products_data = paginator.get_page(page_num)
        totalPages = all_products_data.paginator.num_pages
        data = {'best_products': best_products, 'all_products': all_products_data, 'total_pages': totalPages,
                'current_page': page_num}
        return render(request, "home.html", data)


def products(request):
    if request.method == 'POST':
        product_id = request.POST.get('productID')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {product_id: 1}
        request.session['cart'] = cart
        return redirect('products')
    else:
        all_products = Product.objects.all()
        query = request.GET.get('query')
        filter_price = request.GET.get('filter_price')
        filter_size = request.GET.get('filter_size')
        if query:
            all_products = Product.objects.filter(name__icontains=query)
        if filter_price and filter_price != 'all':
            if filter_price == '0':
                all_products = Product.objects.filter(price__range=(0, 1000))
            elif filter_price == '1000':
                all_products = Product.objects.filter(price__range=(1000, 5000))
            elif filter_price == '5000':
                all_products = Product.objects.filter(price__range=(5000, 10000))
            elif filter_price == '10000':
                all_products = Product.objects.filter(price__gte=10000)
        if filter_size and filter_size != 'all':
            all_products = Product.objects.filter(size=filter_size)
        return render(request, 'products.html', {'all_products': all_products})


@login_required()
@customer_required
def product_page(request, product_id):
    if request.method == 'POST':
        product_id = request.POST.get('productID')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart[product_id] = 1
        request.session['cart'] = cart
        return redirect('product_page', product_id)

    product = Product.objects.get(product_id=product_id)
    return render(request, 'ProductPage.html', {'product': product})


@login_required()
@customer_required
def category(request):
    if request.method == 'POST':
        product_id = request.POST.get('productID')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {product_id: 1}
        request.session['cart'] = cart
        return redirect('category')
    # fetching products according to category
    else:
        oil_painting = Product.objects.filter(category='oil')
        acrylic_painting = Product.objects.filter(category='acrylic')
        water_painting = Product.objects.filter(category='water')
        pastel_painting = Product.objects.filter(category='pastel')
        spray_painting = Product.objects.filter(category='spray')
        other = Product.objects.filter(category='other')
        painting_category = {"oil": oil_painting, "acrylic": acrylic_painting, "water": water_painting,
                             "pastel": pastel_painting, "spray": spray_painting, "other": other}

        return render(request, 'category.html', {'painting_category': painting_category})


@login_required()
@customer_required
def about(request):
    return render(request, 'about.html')


@login_required()
@customer_required
def checkout(request):
    if request.method == 'POST':
        product_id = request.POST.get('productID')
        if product_id:
            remove = request.POST.get('remove')
            cart = request.session.get('cart')
            quantity = cart.get(product_id)
            if remove:
                if quantity == 1:
                    cart.pop(product_id)
                else:
                    cart[product_id] = quantity - 1
            else:
                cart[product_id] = quantity + 1
            request.session['cart'] = cart
            return redirect('checkout')
    form = shippingForm()
    coupon=couponForm()
    cart_products_list = list(request.session.get('cart').keys())
    cart_products = Product.objects.filter(product_id__in=cart_products_list)
    return render(request, 'checkout.html', {'form': form, 'cart_products': cart_products,'coupon':coupon})


@login_required()
@customer_required
def orderConfirmation(request):
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        cart = request.session.get('cart')
        for product_id, quantity in cart.items():
            product = Product.objects.get(product_id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        form = shippingForm(request.POST)
        if form.is_valid():
            shipping_info = form.save(commit=False)
            shipping_info.customer = request.user.customer
            shipping_info.order = order
            shipping_info.save()
            request.session['cart'] = {}
            return render(request, 'orderConfirm.html', {'order_id': order.order_id})
    return redirect('products')


def generate_invoice(request, orderID):
    # Retrieve order and shipping info
    order = get_object_or_404(Order, pk=orderID)
    shipping_info = get_object_or_404(shippingInfo, order=orderID)

    # Create a response object for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{orderID}.pdf"'

    # Create a canvas
    p = canvas.Canvas(response, pagesize=letter)
    p.setTitle(f"Invoice {orderID}")
    width, height = letter

    # Define styles and colors
    title_font = "Helvetica-Bold"
    regular_font = "Helvetica"
    small_font = "Helvetica"
    large_font_size = 16
    regular_font_size = 12
    small_font_size = 10
    primary_color = HexColor('#333333')
    secondary_color = HexColor('#555555')
    accent_color = HexColor('#007BFF')

    # Add company header
    p.setFont(title_font, large_font_size)
    p.setFillColor(primary_color)
    p.drawString(50, height - 70, "ArtGround")

    # Add logo
    img_url = "logo.png"
    img = ImageReader(img_url)
    p.drawImage(img, x=width - 150, y=height - 70, height=30, width=100, mask='auto')

    # Add a separator line
    p.setLineWidth(0.5)
    p.setStrokeColor(secondary_color)
    p.line(50, height - 100, width - 50, height - 100)

    # Add order and customer information
    p.setFont(regular_font, regular_font_size)
    p.drawString(50, height - 160, f"Invoice ID: {orderID}")
    p.drawString(50, height - 180, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(50, height - 200, f"Customer: {shipping_info.first_name} {shipping_info.last_name}")
    p.drawString(50, height - 220, f"Email: {shipping_info.email}")
    p.drawString(50, height - 240, f"Phone: {shipping_info.phoneNumber}")

    # Add shipping address
    p.drawString(50, height - 260, "Shipping Address:")
    p.setFont(small_font, small_font_size)
    p.setFillColor(secondary_color)
    address_y = height - 280
    p.drawString(70, address_y, f"{shipping_info.address1}")
    if shipping_info.address2:
        p.drawString(70, address_y - 20, f"{shipping_info.address2}")
        address_y -= 20
    p.drawString(70, address_y - 20, f"{shipping_info.City}, {shipping_info.State}, {shipping_info.Country}")
    p.drawString(70, address_y - 40, f"Postal Code: {shipping_info.zipCode}")

    # Add payment method
    p.setFillColor(primary_color)
    p.setFont(regular_font, regular_font_size)
    p.drawString(50, address_y - 70, f"Payment Method: {shipping_info.get_paymentType_display()}")

    # Add order items table
    p.setFont(title_font, regular_font_size)
    p.drawString(50, address_y - 100, "Order Items")

    # Table headers
    p.setFont(title_font, small_font_size)
    p.setFillColor(black)
    p.drawString(50, address_y - 120, "Product")
    p.drawString(200, address_y - 120, "Quantity")
    p.drawString(300, address_y - 120, "Price")
    p.drawString(400, address_y - 120, "Total")

    y = address_y - 140
    total_amount = 0
    order_items = order.order_items.all()

    # Table rows
    if order_items.exists():
        for item in order_items:
            p.setFont(regular_font, small_font_size)
            p.setFillColor(secondary_color)
            p.drawString(50, y, f"{item.product.name}")
            p.drawString(200, y, f"{item.quantity}")
            p.drawString(300, y, f"Rs{item.price}")
            total = item.quantity * item.price
            p.drawString(400, y, f"Rs{total}")
            total_amount += total
            y -= 20
    else:
        p.setFont(regular_font, regular_font_size)
        p.setFillColor(primary_color)
        p.drawString(50, y, "No items found in the order.")

    # Add total amount
    p.setFont(title_font, regular_font_size)
    p.setFillColor(primary_color)
    p.drawString(50, y - 40, f"Total Amount: Rs{total_amount}")

    # Add footer with company details
    p.setLineWidth(0.5)
    p.setStrokeColor(secondary_color)
    p.line(50, 100, width - 50, 100)
    p.setFont(regular_font, small_font_size)
    p.setFillColor(secondary_color)
    p.drawString(50, 70, "Thank you for Shopping!")
    p.drawString(50, 55, "If you have any questions about this invoice, please contact us.")
    p.drawString(50, 35, "ArtGround, India | contact@artground.com | +1 (234) 567-890")

    # Finalize the PDF
    p.showPage()
    p.save()

    return response


@login_required()
@customer_required
def OrdersHistory(request):
    order_items = []
    current_user_orders = Order.objects.filter(user=request.user)
    for order in current_user_orders:
        order_items = order.order_items.all()

    return render(request, 'PurchasedHistory.html', {'purchase_history': order_items})
