from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from Account.decorators import seller_required
from .forms import productForm
from .models import Product


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
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES)
        print("form submitted")
        if form.is_valid():
            print("form is valid")
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            return redirect('sellerHome')
    else:
        form = productForm()
    return render(request, 'productForm.html', {'form': form})


def allProducts(request):
    products = Product.objects.filter(seller=request.user.seller)
    return render(request, 'sellerProducts.html', {'products': products})


@login_required()
@seller_required
def editProduct(request, productID):
    product=get_object_or_404(Product,pk=productID,seller=request.user.seller)
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            return redirect('allProducts')
    else:
        form = productForm(instance=product)
    return render(request, 'productForm.html', {'form': form})


@login_required()
@seller_required
def deleteProduct(request,productID):
    product=get_object_or_404(Product,pk=productID,seller=request.user.seller)
    if request.method == 'POST':
        product.delete()
        return redirect('allProducts')
    return render(request, 'sellerHome.html')
