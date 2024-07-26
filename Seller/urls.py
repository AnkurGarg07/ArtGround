from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.sellerHome, name='sellerHome'),
    path('home/addProducts', views.addProducts, name='addProducts'),
    path('home/allProducts', views.allProducts, name='allProducts'),
    path('home/TotalSales', views.TotalSales, name='TotalSales'),
    path('home/editProducts/<productID>', views.editProduct, name='editProducts'),
    path('home/deleteProducts/<productID>', views.deleteProduct, name='deleteProducts')
]
