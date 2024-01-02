from django.shortcuts import redirect, render
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm


# Create your views here.
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {"product": product})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html", {"categories": categories})


def category(request, foo):
    # Replace Hyphens with Spaces
    foo = foo.replace("-", " ")
    # Grab the category from the url
    try:
        # Look Up The Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(
            request, "category.html", {"products": products, "category": category}
        )
    except:
        messages.success(request, ("That Category Doesn't Exist..."))
        return redirect("home")


def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


def about(request):
    return render(request, "about.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have Been Logged In !"))
            return redirect("home")
        else:
            messages.success(request, ("There was an error please try again !"))
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    messages.success(request, ("You have Been Logout In!"))
    logout(request)
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("you have registered successfully "))
            return redirect("home")
        else:
            messages.success(request, ("There was an error please try again !"))
            return redirect("register")

    else:
        return render(request, "register.html", {"form": form})
