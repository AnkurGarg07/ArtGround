from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Account.decorators import customer_required, seller_required


@login_required()
@customer_required
def home(request):
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

    all_products = [
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
        {
            id: 6,
            'image': "../../static/assets/products/product-2.png",
            'title': "Long Head Birds",
            'owner': "Inkset Painter",
            'price': "899",
        },
        {
            id: 7,
            'image': "../../static/assets/products/product-3.png",
            'title': "3D Flower Pot",
            'owner': "The 3D World",
            'price': "1299",
        },
        {
            id: 8,
            'image': "../../static/assets/products/product-4.png",
            'title': "The Horse Rider",
            'owner': "OilyHands",
            'price': "999",
        },
        {
            id: 9,
            'image': "../../static/assets/products/product-1.png",
            'title': "Vintage Car",
            'owner': "Digiland Art Sage",
            'price': "449",
        },
        {
            id: 10,
            'image': "../../static/assets/products/product-2.png",
            'title': "Long Head Birds",
            'owner': "Inkset Painter",
            'price': "899",
        },
    ]

    return render(request, 'Customer/home.html', {'best_products': best_products, 'all_products': all_products})


@login_required()
@customer_required
def about(request):
    return render(request, 'Customer/about.html')


@login_required()
@customer_required
def category(request):
    return render(request, 'Customer/category.html')


@login_required()
@customer_required
def cart(request):
    return render(request, 'Customer/cart.html')


@login_required()
@customer_required
def checkout(request):
    return render(request, 'Customer/checkout.html')


@login_required()
@customer_required
def orderConfirmation(request):
    return render(request, 'Customer/orderConfirm.html')
