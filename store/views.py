import json
from cart.cart import Cart
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from payment.models import ShippingAddress

from .models import Product, Category, Profile
from .forms import UserUpdateForm, UserProfileForm
from payment.forms import ShippingAddressForm


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


def about(request):
    return render(request, "store/about.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            current_user = Profile.objects.filter(user__id=request.user.id)
            saved_cart = current_user[0].old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                cart.load(converted_cart)
            return redirect("home")
        else:
            messages.error(request, "Login failed")
            return redirect("login")
    else:
        form = AuthenticationForm()
        return render(request, "store/login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect("update_profile")
        else:
            messages.error(request, "Account creation failed")
            return redirect("register")
    else:
        form = UserCreationForm()
    return render(request, "store/register.html", {"form": form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = UserUpdateForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "Account updated successfully")
            return redirect("home")
        return render(request, "store/update_user.html", {"form": form})
    else:
        messages.error(request, "You must be logged in to update your account")
        return redirect("login")


def update_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to update your password")
        return redirect("login")
    user_profile = Profile.objects.get(user__id=request.user.id)
    user_shipping = ShippingAddress.objects.get(user__id=request.user.id)
    form = UserProfileForm(request.POST or None, instance=user_profile)
    shipping_form = ShippingAddressForm(request.POST or None, instance=user_shipping)
    if request.method == "POST":
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, "Profile updated successfully!")
        elif shipping_form.is_valid() and shipping_form.has_changed():
            shipping_form.save()
            messages.success(request, "Shipping address updated successfully!")
        return redirect("home")
    return render(
        request,
        "store/update_profile.html",
        {"form": form, "shipping_form": shipping_form},
    )


def update_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to update your password")
        return redirect("login")
    form = SetPasswordForm(request.user, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Password updated successfully! Please log in again to continue",
            )
            return redirect("login")
    return render(request, "store/update_password.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "Account logged out successfully")
    return redirect("home")


def product(request, id):
    product = Product.objects.get(id=id)
    return render(request, "store/product.html", {"product": product})


def category(request, name):
    name = name.replace("-", " ")
    try:
        category = Category.objects.filter(name=name)
        category = category[0]
        products = Product.objects.filter(category=category)
        return render(
            request, "store/category.html", {"products": products, "category": category}
        )
    except Product.DoesNotExist:
        messages.error(request, "Category does not exist")
        return redirect("home")


def category_summary(request):
    categories = Category.objects.all()
    return render(request, "store/category_summary.html", {"categories": categories})


def search(request):
    if request.method == "POST":
        query = request.POST.get("query")
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        if not products:
            messages.error(request, "No search results found")
        return render(
            request, "store/search.html", {"query": query, "products": products}
        )
    return render(request, "store/search.html", {})
