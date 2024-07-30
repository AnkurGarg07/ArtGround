from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from Customer.models import shippingInfo
from Account.decorators import customer_required
from Customer.forms import shippingForm
from Seller.models import Product, Order, OrderItem


@login_required()
@customer_required
def home(request):
    # print(request.session['cart'])
    best_products = [
        {
            id: 1,
            'image': "../../static/assets/products/product-1.png",
            'title': "Vintage Car",
            'owner': "Digiland Art Sage",
            'price': "449",
        },
        {
            id: 2,
            'image': "../../static/assets/products/product-2.png",
            'title': "Long Head Birds",
            'owner': "Inkset Painter",
            'price': "899",
        },
        {
            id: 3,
            'image': "../../static/assets/products/product-3.png",
            'title': "3D Flower Pot",
            'owner': "The 3D World",
            'price': "1299",
        },
        {
            id: 4,
            'image': "../../static/assets/products/product-4.png",
            'title': "The Horse Rider",
            'owner': "OilyHands",
            'price': "999",
        },
        {
            id: 5,
            'image': "../../static/assets/products/product-1.png",
            'title': "Vintage Car",
            'owner': "Digiland Art Sage",
            'price': "449",
        },
    ]
    #handling if product is added
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
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        return redirect('home')

    #handling normal open of home page
    else:
        all_products = Product.objects.all()
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
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        return redirect('products')
    else:
        products = Product.objects.all()
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__icontains=query)
        return render(request, 'products.html', {'all_products': products})


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
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
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
    cart_products_list = list(request.session.get('cart').keys())
    cart_products = Product.objects.filter(product_id__in=cart_products_list)
    return render(request, 'checkout.html', {'form': form, 'cart_products': cart_products})


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
            messages.success(request, 'Your order has been placed successfully!')
            request.session['cart'] = {}
            return render(request, 'orderConfirm.html', {'order_id': order.order_id})
    return redirect('products')


def generate_invoice(request, orderID):
    order = get_object_or_404(Order, pk=orderID)
    shipping_info = get_object_or_404(shippingInfo, order=orderID)
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    # Add title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Invoice #{orderID}")
    # Add order and customer information
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(50, height - 100, f"Customer: {shipping_info.first_name} {shipping_info.last_name}")
    p.drawString(50, height - 120, f"Email: {shipping_info.email}")
    p.drawString(50, height - 140, f"Phone: {shipping_info.phoneNumber}")
    p.drawString(50, height - 160, "Shipping Address:")
    p.drawString(70, height - 180, f"{shipping_info.address1}")
    if shipping_info.address2:
        p.drawString(70, height - 200, f"{shipping_info.address2}")
        p.drawString(70, height - 220, f"{shipping_info.City}, {shipping_info.State}, {shipping_info.Country}")
    else:
        p.drawString(70, height - 200, f"{shipping_info.City}, {shipping_info.State}, {shipping_info.Country}")
    p.drawString(50, height - 240, f"Postal Code: {shipping_info.zipCode}")
    p.drawString(50, height - 260, f"Payment Method: {shipping_info.get_paymentType_display()}")
    # Add order items
    p.drawString(50, height - 300, "Order Items:")
    p.drawString(70, height - 320, "Product")
    p.drawString(270, height - 320, "Quantity")
    p.drawString(370, height - 320, "Price")
    p.drawString(470, height - 320, "Total")
    y = height - 340
    total_amount = 0
    order_items = order.order_items.all()

    if order_items.exists():
        for item in order_items:
            p.drawString(70, y, f"{item.product.name}")
            p.drawString(270, y, f"{item.quantity}")
            p.drawString(370, y, f"Rs{item.price}")
            total = item.quantity * item.price
            p.drawString(470, y, f"Rs{total}")
            total_amount += total
            y -= 20
    else:
        p.drawString(70, y, "No items found in the order.")

    p.drawString(50, y - 40, f"Total Amount: Rs{total_amount}")
    p.showPage()
    p.save()
    return response

@login_required()
@customer_required
def PurchasedHistory(request):
    product_purchased = [
        {
            'id': 1,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "Vintage Car",
            'price': "449",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 2,
            'image': "http://127.0.0.1:8000/media/product_images/IMG-20240629-WA0010.jpg",
            'title': "Long Head Birds",
            'price': "899",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 3,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "3D Flower Pot",
            'price': "1299",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 4,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "The Horse Rider",
            'price': "999",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 5,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "Vintage Car",
            'price': "449",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 1,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "Vintage Car",
            'price': "449",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 2,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "Long Head Birds",
            'price': "899",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 3,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "3D Flower Pot",
            'price': "1299",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 4,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "The Horse Rider",
            'price': "999",
            'date': "2021-09-12",
            'invoice': "/"
        },
        {
            'id': 5,
            'image': "http://127.0.0.1:8000/media/product_images/product-2_RqrGpek.png",
            'title': "Vintage Car",
            'price': "449",
            'date': "2021-09-12",
            'invoice': "/"
        },
    ]

    return render(request, 'PurchasedHistory.html', {'purchase_history': product_purchased})
