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
from Customer.models import shippingInfo, couponInfo, productReview
from Account.decorators import customer_required
from Customer.forms import shippingForm, couponForm, reviewForm
from Seller.models import Product, Order, OrderItem
from django.db.models import Avg
import requests

from ArtGround.vars import EMAIL_ID, EMAIL_PASSWORD, ENTERPRISE_KEY


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
        best_products = Product.objects.all().order_by('-rating')[:best_products_limit]
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
                'current_page': page_num, 'title': "Home"}
        return render(request, "home.html", data)


@login_required()
@customer_required
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
        filter_rating=request.GET.get('filter_rating')
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
        if filter_rating and filter_rating != 'all':
            lower_bound = int(filter_rating)
            upper_bound = lower_bound + 1
            all_products = Product.objects.filter(rating__gte=lower_bound, rating__lt=upper_bound)
        return render(request, 'products.html', {'all_products': all_products, 'title': "All Products"})


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
    similar_products = Product.objects.filter(category=product.category).exclude(product_id=product_id)
    reviews = productReview.objects.filter(product=product)
    return render(request, 'ProductPage.html',
                  {'product': product, 'similar_products': similar_products, 'reviews': reviews})


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

        return render(request, 'category.html', {'painting_category': painting_category, "title": "Category Products"})


@login_required()
@customer_required
def about(request):
    return render(request, 'about.html', {"title": "About Us"})

@login_required()
@customer_required
def privacy(request):
    return render(request, 'privacy-policy.html', {"title": "Privacy Policy"})

@login_required()
@customer_required
def terms_condition(request):
    return render(request, 'terms_condition.html', {"title": "Terms & Condition"})


@login_required()
@customer_required
def checkout(request):
    if request.method == 'POST':
        product_id = request.POST.get('productID')
        coupon_code = request.GET.get('code')
        print(coupon_code)
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
            if coupon_code is None:
                return redirect('checkout')
            else:
                return redirect(f'/checkout/?code={coupon_code}')
    form = shippingForm()
    coupon_code = request.GET.get('code')
    coupon_discount = 0
    coupon_code_exists = None
    if coupon_code:
        coupon_code_exists = couponInfo.objects.filter(code__iexact=coupon_code).exists()
        if coupon_code_exists:
            coupon = couponInfo.objects.get(code__iexact=coupon_code)
            coupon_discount = coupon.discount
    coupon = couponForm()
    cart_products_list = list(request.session.get('cart').keys())
    cart_products = Product.objects.filter(product_id__in=cart_products_list)
    return render(request, 'checkout.html',
                  {'form': form, 'cart_products': cart_products, 'coupon': coupon,
                   'coupon_code_exists': coupon_code_exists, 'coupon_discount': coupon_discount})


def send_email(request, email_value, order_items_html, order_id):
    url = 'https://mail.dwine.me/api/v1/send-mail/enterprise'
    
    payload = {
        "authUser": EMAIL_ID,
        "authPass": EMAIL_PASSWORD,
        "EnterpriseKey": ENTERPRISE_KEY,
        "To": email_value,
        "FromName": "ArtGround",
        "ReplyAddress": EMAIL_ID,
        "Subject": f"Your Order has been Placed Successfully",
        "Body": f"""
        <table
            style="
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                font-family: Arial, sans-serif;
                border-spacing: 0;
                background-color: #f9f9f9;
                border: 1px solid #e9e9e9;
                padding: 10px;
                border-radius: 15px;
            "
            >
            <tr>
                <td
                style="
                    padding: 20px;
                    text-align: center;
                    background-color: #4a68a9;
                    border-radius: 10px 10px 0px 0px;
                "
                >
                <h1 style="color: #ffffff; margin: 0;">ArtGround</h1>
                <p style="color: #ffffff; margin-top: 10px;">
                    Your Order Has Been Placed!
                </p>
                </td>
            </tr>
            <tr>
                <td style="padding: 30px; background-color: #ffffff;">
                <p
                    style="
                    font-size: 16px;
                    color: #333333;
                    line-height: 1.5;
                    margin: 0 0 20px;
                    "
                >
                    Hi there,
                </p>
                <p
                    style="
                    font-size: 16px;
                    color: #333333;
                    line-height: 1.5;
                    margin: 0 0 20px;
                    "
                >
                    We're excited to let you know that we've successfully received your
                    order! Here's a summary of your purchase:
                </p>

                <p
                    style="
                    font-size: 16px;
                    color: #333333;
                    line-height: 1.5;
                    margin: 0 0 20px;
                    "
                >
                    <strong style="color: #4a68a9;">Order ID: {order_id}</strong>
                </p>

                <table style="width: 100%; margin-top: 20px; border-spacing: 0;">
                    {order_items_html}
                </table>

                <p
                    style="
                    font-size: 16px;
                    color: #333333;
                    line-height: 1.5;
                    margin: 0 0 20px;
                    "
                >
                    You'll receive a notification with your shipping details as soon as your
                    order is on its way. If you have any questions or need further
                    assistance, feel free to reach out to us.
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.5; margin: 0;">
                    Thanks for choosing ArtGround!<br />
                    The ArtGround Team
                </p>
                </td>
            </tr>
            <tr>
                <td
                style="
                    padding: 15px;
                    text-align: center;
                    background-color: #4a68a9;
                    border-radius: 0px 0px 10px 10px;
                "
                >
                <p style="color: #ffffff; font-size: 12px; margin: 0;">
                    © 2024 ArtGround | All rights reserved
                </p>
                </td>
            </tr>
        </table>
        """,
        }

    headers = {
            'Content-Type': 'application/json',
        }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            messages.success(request, "Email sent successfully.")
        else:
            messages.error(request, f"Failed to send email. Status Code: {response.status_code}")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")


@login_required()
@customer_required
def orderConfirmation(request):
    if request.method == 'POST':
        order_items_html = ''
        order = Order.objects.create(user=request.user)
        cart = request.session.get('cart')
        for product_id, quantity in cart.items():

            product = Product.objects.get(product_id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            order_items_html += f"""
                        <tr>
                            <td style="padding: 10px; text-align: left; display:flex; width:100%;">
                                <p style="margin: 0; font-weight: bold;">{product.name} | {product.price}</p>
                            </td>
                        </tr>
                        """
        form = shippingForm(request.POST)
        send_email(request, request.user.email, order_items_html, order.order_id)
        if form.is_valid():
            shipping_info = form.save(commit=False)
            shipping_info.customer = request.user.customer
            shipping_info.order = order
            shipping_info.save()
            request.session['cart'] = {}
            return render(request, 'orderConfirm.html', {'order_id': order.order_id, 'title': "Order Confirmation"})
    return redirect('products')


@login_required()
@customer_required
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
    if request.method == 'POST':
        form = reviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            productID = request.POST.get('productID')
            review.user = request.user.customer
            product = Product.objects.get(product_id=productID)
            review.product = product
            review.save()
            average_rating = productReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
            if average_rating is not None:
                product.rating = average_rating
                product.save()
            return redirect('Orders')
    review = reviewForm()
    order_items = []
    current_user_orders = Order.objects.filter(user=request.user)
    for order in current_user_orders:
        order_items += order.order_items.all()

    return render(request, 'PurchasedHistory.html', {'purchase_history': order_items, 'review': review})
