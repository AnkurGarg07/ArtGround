from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<str:product_id>', views.product_page, name='product_page'),
    path('category/', views.category, name='category'),
    path('about-us/', views.about, name='about-us'),
    path('privacy-policy/', views.privacy, name='privacy-policy'),
    path('terms-and-condition/', views.terms_condition, name='terms-and-condition'),
    path('checkout/', views.checkout, name='checkout'),
    # path('checkoutHandle', views.checkoutHandle, name='checkoutHandle'),
    path('orderConfirmation/', views.orderConfirmation, name='orderConfirmation'),
    path('invoice/<str:orderID>/pdf/', views.generate_invoice, name='generate_invoice_pdf'),
    path('Orders/', views.OrdersHistory, name='Orders'),
]
