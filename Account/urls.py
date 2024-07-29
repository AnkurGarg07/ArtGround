from django.urls import path,include
from . import views



urlpatterns = [
    # path('login/', views.login_view, name='login'),
    path('register/Customer/', views.register_customer, name='register_customer'),
    path('register/seller/', views.register_seller, name='register_seller'),
    path('login/Customer/', views.login_customer, name='login_customer'),
    path('login/seller/', views.login_seller, name='login_seller'),
    path('logout/customer',views.logout_view,name='logout_customer'),
    path('logout/seller',views.logout_to_seller,name='logout_seller'),
]

