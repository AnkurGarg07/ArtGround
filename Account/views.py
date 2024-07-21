# views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_backends

from .decorators import redirect_if_logged_in
from .forms import RegistrationForm, CustomerProfileForm, SellerProfileForm, CustomLoginForm
from .models import Seller, Customer, User

@redirect_if_logged_in
def register(request, user_type):
    profile_form = None
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if user_type == 'customer':
                user.is_customer = True
                profile_form = CustomerProfileForm(request.POST)
            elif user_type == 'seller':
                user.is_seller = True
                profile_form = SellerProfileForm(request.POST)
            user.save()

            if profile_form and profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                login(request, user, backend='Account.backends.EmailBackend')  # Use Django's login method
                if user.is_customer:
                    return redirect('index')
                elif user.is_seller:
                    return redirect('seller')
            else:
                messages.error(request, 'Profile form is invalid. Please correct the errors below.')
        else:
            messages.error(request, 'Email id already registered.')
            # If user_form is invalid, reinitialize the profile_form
            if user_type == 'customer':
                profile_form = CustomerProfileForm()
            elif user_type == 'seller':
                profile_form = SellerProfileForm()
    else:
        user_form = RegistrationForm()
        if user_type == 'customer':
            profile_form = CustomerProfileForm()
        elif user_type == 'seller':
            profile_form = SellerProfileForm()

    heading = 'Customer' if user_type == 'customer' else 'Seller'
    return render(request, 'Account/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'heading': heading
    })

@redirect_if_logged_in
def register_seller(request):
    return register(request, 'seller')

@redirect_if_logged_in
def register_customer(request):
    return register(request, 'customer')

@redirect_if_logged_in
def login_seller(request):
    return login_view(request, 'seller')

@redirect_if_logged_in
def login_customer(request):
    return login_view(request, 'customer')

@redirect_if_logged_in
def login_view(request, user_type):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password, backend='Account.backends.EmailBackend')
            if user is not None:
                if (user_type == 'seller' and user.is_seller) or (user_type == 'customer' and user.is_customer):
                    login(request, user)
                    if user.is_customer:
                        return redirect('index')  # Replace with actual URL name
                    elif user.is_seller:
                        return redirect('seller')  # Replace with actual URL name
                else:
                    # User type mismatch
                    messages.error(request, 'Invalid credentials for this login page.')
            else:
                print("Authentication failed: Invalid credentials")
                messages.error(request, 'Invalid Credentials')
        else:
            messages.error(request, 'Form invalid')
    else:
        form = CustomLoginForm()
    heading = 'Seller' if user_type == 'seller' else 'Customer'
    return render(request, 'account/login.html', {'form': form, 'heading': heading})


def logout_view(request):
    user = request.user
    logout(request)
    return redirect('login_customer')
