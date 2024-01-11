from django.shortcuts import redirect, render, get_object_or_404
from .models import Movie, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Actor
from .forms import MovieForm, ActorForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.urls import reverse


@login_required
def like_product(request, pk):
    product = Movie.objects.get(id=pk)

    if request.user in product.likes.all():
        product.likes.remove(request.user)
        like = product.likes
    else:
        product.likes.add(request.user)
        like = product.likes
        return render(request, "product.html", {"product": product, "like": like})
    return render(request, "product.html", {"product": product, "like": like})


def product(request, pk):
    product = Movie.objects.get(id=pk)
    like = product.likes
    return render(request, "product.html", {"product": product, "like": like})


def category_summary(request):
    categories = Category.objects.all()
    return redirect(request, "category_summary.html", {"categories": categories})


def category(request, foo):
    # Replace Hyphens with Spaces
    foo = foo.replace("-", " ")
    # Grab the category from the url
    try:
        # Look Up The Category
        category = Category.objects.get(name=foo)
        products = Movie.objects.filter(category=category)
        return render(
            request, "category.html", {"products": products, "category": category}
        )
    except:
        messages.success(request, ("That Category Doesn't Exist..."))
        return redirect("home")


def home(request):
    if User.is_anonymous:
        products = Movie.objects.all()
        return render(
            request,
            "home.html",
            {
                "products": products,
            },
        )
    else:
        profile = request.user.profile
        products = Movie.objects.all()

        return render(
            request,
            "home.html",
            {"products": products, "profile": profile},
        )


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


@login_required
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect("home")

    else:
        form = MovieForm()

    return render(request, "add_movie.html", {"form": form})


@login_required
def update_movie(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            like = movie.likes
            return render(request, "product.html", {"product": movie, "like": like})
    else:
        form = MovieForm(instance=movie)

    return render(request, "update_movie.html", {"form": form, "movie": movie})


@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, id=pk)

    if request.method == "POST":
        movie.delete()
        return redirect("home")

    return render(request, "delete_movie.html", {"movie": movie})


@login_required
def add_actor(request):
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            actor = form.save()
            actors = Actor.objects.all()
            return render(request, "all_actors.html", {"actors": actors})
    else:
        form = ActorForm()

    return render(request, "add_actor.html", {"form": form})


@login_required
def update_actor(request, pk):
    actor = get_object_or_404(Actor, pk=pk)

    if request.method == "POST":
        form = ActorForm(request.POST, instance=actor)
        if form.is_valid():
            actor = form.save()
            actors = Actor.objects.all()
            return render(request, "all_actors.html", {"actors": actors})
    else:
        form = ActorForm(instance=actor)

    return render(request, "update_actor.html", {"form": form, "actor": actor})


@login_required
def delete_actor(request, pk):
    actor = get_object_or_404(Actor, pk=pk)

    if request.method == "POST":
        actor.delete()
        actors = Actor.objects.all()
        return render(request, "all_actors.html", {"actors": actors})

    return render(request, "delete_actor.html", {"actor": actor})


def all_actors(request):
    actors = Actor.objects.all()
    return render(request, "all_actors.html", {"actors": actors})
