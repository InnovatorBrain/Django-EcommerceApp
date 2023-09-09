from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection
from .serializer import ProductSerializer
from .serializer import CollectionSerializer
from .serializer import ReviewSerializer
from .serializer import CartItemSerializer
from .serializer import CartSerializer
from rest_framework import status


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


    def destroy(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(
            "Product deleted successfully", status=status.HTTP_204_NO_CONTENT
            )
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def delete(self, request, pk):
        collection = Collection.objects.get(pk=pk)
        collection.delete()
        return Response(
            "Collection deleted successfully", status=status.HTTP_204_NO_CONTENT
        )

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Product.objects.get(pk=self.kwargs["product_pk"]).reviews.all()

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}