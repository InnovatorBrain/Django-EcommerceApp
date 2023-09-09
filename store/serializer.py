from rest_framework import serializers
from .models import Product, Collection, Cart, CartItem, Review
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source="unit_price"
    )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(), view_name="collection-detail"
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "inventory",
            "price",
            "price_with_tax",
            "collection",
        ]

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "created_at"]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["name", "email", "description", "date"]
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)
