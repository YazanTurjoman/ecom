from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user
import datetime


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Actor(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="upload/actor/")

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="upload/product/")
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    likes = models.ManyToManyField(User, related_name="movie_likes", blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.today)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    # Additional Fields
    director = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)

    # ManyToMany Relationship with Actor
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)

    # Methods for Additional Functionality
    def is_on_sale(self):
        return self.is_sale and self.sale_price < self.price

    def get_formatted_release_date(self):
        return (
            self.release_date.strftime("%B %d, %Y")
            if self.release_date
            else "Not specified"
        )

    def total_likes(self):
        return self.likes.count()

    def liked(self):
        return self.likes.all()

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Movie, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=250, default="", blank=True)
    phone = models.CharField(max_length=10, default="", blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
