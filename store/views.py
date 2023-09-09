from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Product, Collection
from .serializer import ProductSerializer
from .serializer import CollectionSerializer
from .serializer import CartItemSerializer
from .serializer import CartSerializer
from rest_framework import status


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(
            "Product deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class CollectionDetail(APIView):
    def get(self, request, pk):
        try:
            collection = Collection.objects.get(pk=pk)
            serializer = CollectionSerializer(collection, context={"request": request})
            return Response(serializer.data)
        except Collection.DoesNotExist:
            return Response("Collection not found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collection = Collection.objects.get(pk=pk)
        collection.delete()
        return Response(
            "Collection deleted successfully", status=status.HTTP_204_NO_CONTENT
        )
