from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps


def customer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated:
            # Redirect authenticated sellers to their home page
            return redirect('seller')
        return redirect('login_customer')

    return _wrapped_view


def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated:
            # Redirect authenticated customers to their home page
            return redirect('index')
        return redirect('login_seller')

    return _wrapped_view

def redirect_if_logged_in(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_customer:
                return redirect('index')  # Replace with your actual customer home page URL name
            elif request.user.is_seller:
                return redirect('seller')  # Replace with your actual seller home page URL name
        return view_func(request, *args, **kwargs)
    return _wrapped_view
