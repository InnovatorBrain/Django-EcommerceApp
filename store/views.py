from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializer import ProductSerializer
from .serializer import CollectionSerializer
from .serializer import ReviewSerializer
from .models import Product, Collection
from .filters import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

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


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Product.objects.get(pk=self.kwargs["product_pk"]).reviews.all()

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
