from django.shortcuts import render
from django.views import View
from .models import Category,Product

def product_list(request):
    products = Product.products.all()
    context = {
            "products":products,
        }
    return render(request, "store/index.html", context)