from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Account.decorators import seller_required
from .forms import productForm

# Create your views here.
@login_required()
@seller_required
def sellerHome(request):
    print(request.session['seller'])
    return render(request, 'sellerHome.html')


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
