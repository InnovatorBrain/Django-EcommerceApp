from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializer import ProductSerializer
from .serializer import CollectionSerializer
from rest_framework import status

@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Product created successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", 'DELETE'])
def product_detail(request, id):
    product = Product.objects.get(pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        product.delete()
        return Response("Product deleted successfully", status=status.HTTP_204_NO_CONTENT)

@api_view(["GET", "POST"])

def collection_list(request):
    if request.method == "GET":
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Collection created successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    if request.method == "GET":
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collection, context={'request': request})
        return Response(serializer.data)
    elif request.method == "PUT":
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        collection = Collection.objects.get(pk=pk)
        collection.delete()
        return Response("Collection deleted successfully", status=status.HTTP_204_NO_CONTENT)







