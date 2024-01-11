from django.contrib import admin
from .models import Category, Customer, Movie, Order, Actor

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Movie)
admin.site.register(Order)
admin.site.register(Actor)
