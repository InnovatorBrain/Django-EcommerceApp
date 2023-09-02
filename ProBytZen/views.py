from django.shortcuts import render
from store.models import Product

# Create your views here.
# We also use this file to manupolate Django with ORM


def index(request):
    product = Product.objects.filter(title__icontains="cof")
    print(product)
    return render(request, "index.html")
