from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.decorators import api_view

# from rest_framework.response import Response
from rest_framework.response import Response
from .models import Product, Collection
from .serializer import ProductSerializer
from .serializer import CollectionSerializer

from rest_framework import status


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the validated data to create a new Product instance
            return Response("Product created successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=404)


@api_view()
def collection_detail(request, pk):
    collection = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
