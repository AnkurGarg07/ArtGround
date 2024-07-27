from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from Account.decorators import customer_required, seller_required
from Customer.forms import shippingForm
from Seller.models import Product


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
        print("outer")
        if product_id:
            print(product_id)
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

        form = shippingForm(request.POST)
        print(request.user)
        if form.is_valid():
            shippingInfo = form.save(commit=False)
            shippingInfo.customer = request.user.customer
            shippingInfo.save()
            messages.success(request, 'Your shipping has been done!')
            return redirect('orderConfirmation')
        else:
            print("Form invalid")
            print(form.errors)
    else:
        form = shippingForm()
    cart_products_list = list(request.session.get('cart').keys())
    cart_products = Product.objects.filter(product_id__in=cart_products_list)
    return render(request, 'checkout.html', {'form': form, 'cart_products': cart_products})


@login_required()
@customer_required
def orderConfirmation(request):
    return render(request, 'orderConfirm.html')


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
