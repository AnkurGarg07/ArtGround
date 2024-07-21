from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from Account.decorators import customer_required, seller_required
from Seller.models import Product


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

    all_products = Product.objects.all()
    paginator = Paginator(all_products, 10)
    page_num = request.GET.get('page')
    if not page_num:
        page_num = 1
    all_products_data = paginator.get_page(page_num)
    totalPages = all_products_data.paginator.num_pages
    data = {'best_products': best_products, 'all_products': all_products_data, 'total_pages': totalPages,
            'current_page': page_num}
    return render(request, 'Customer/home.html', data)


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
def checkout(request):
    return render(request, 'Customer/checkout.html')


@login_required()
@customer_required
def orderConfirmation(request):
    return render(request, 'Customer/orderConfirm.html')
