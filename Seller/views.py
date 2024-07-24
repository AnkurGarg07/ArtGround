from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Account.decorators import seller_required
from .forms import productForm

# Create your views here.
@login_required()
@seller_required
def sellerHome(request):
    product_sales = [
        {
            'id': 1,
            'image': "../../static/assets/products/product-1.png",
            'title': "Vintage Car",
            'price': "449",
            'sales': "325",
        },
        {
            'id': 2,
            'image': "../../static/assets/products/product-2.png",
            'title': "Long Head Birds",
            'price': "899",
            'sales': "315",
        },
        {
            'id': 3,
            'image': "../../static/assets/products/product-3.png",
            'title': "3D Flower Pot",
            'price': "1299",
            'sales': "65",
        },
        {
            'id': 4,
            'image': "../../static/assets/products/product-4.png",
            'title': "The Horse Rider",
            'price': "999",
            'sales': "135",
        },
        {
            'id': 5,
            'image': "../../static/assets/products/product-1.png",
            'title': "Vintage Car",
            'price': "449",
            'sales': "353",
        },
        {
            'id': 1,
            'image': "../../static/assets/products/product-1.png",
            'title': "Vintage Car",
            'price': "449",
            'sales': "115",
        },
        {
            'id': 2,
            'image': "../../static/assets/products/product-2.png",
            'title': "Long Head Birds",
            'price': "899",
            'sales': "325",
        },
        {
            'id': 3,
            'image': "../../static/assets/products/product-3.png",
            'title': "3D Flower Pot",
            'price': "1299",
            'sales': "252",
        },
        {
            'id': 4,
            'image': "../../static/assets/products/product-4.png",
            'title': "The Horse Rider",
            'price': "999",
            'sales': "332",
        },
        {
            'id': 5,
            'image': "../../static/assets/products/product-1.png",
            'title': "Vintage Car",
            'price': "449",
            'sales': "62",
        },
    ]

    return render(request, 'sellerHome.html', {'product_sales': product_sales})


@login_required()
@seller_required
def addProducts(request):
    form = productForm()
    return render(request, 'productForm.html', {'form': form})


@login_required()
@seller_required
def editProduct(request):
    return render(request, 'productForm.html')


@login_required()
@seller_required
def deleteProduct(request):
    return render(request, 'sellerHome.html')
