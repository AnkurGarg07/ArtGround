from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<str:product_id>', views.product_page, name='product_page'),
    path('category/', views.category, name='category'),
    path('about/', views.about, name='about'),
    path('checkout/', views.checkout, name='checkout'),
    # path('checkoutHandle', views.checkoutHandle, name='checkoutHandle'),
    path('orderConfirmation/', views.orderConfirmation, name='orderConfirmation'),
    path('PurchasedHistory/', views.PurchasedHistory, name='PurchasedHistory'),
]
