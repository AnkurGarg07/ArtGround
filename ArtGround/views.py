from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from Account.decorators import seller_required,customer_required


@login_required()
@customer_required
def index(request):
    return render(request, 'index.html')


@login_required()
@seller_required
def sellers(request):
    return render(request, 'sellerIndex.html')
