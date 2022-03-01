from django.shortcuts import render
from shop_app.models import Product, Category
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'

class ProductDetails(DetailView, LoginRequiredMixin):
    context_object_name = 'product'
    model = Product
    template_name = 'shop_app/product_detail.html'
