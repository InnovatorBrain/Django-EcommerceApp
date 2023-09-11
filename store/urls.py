from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# Create the main router
router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("carts", views.CartViewSet)

# Create a nested router for cart items
cart_router = routers.NestedSimpleRouter(router, r"carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
    # Add a URL pattern for the collection detail view
    path(
        "collections/<int:pk>/",
        views.CollectionViewSet.as_view({"get": "retrieve"}),
        name="collection-detail",
    ),
    path("carts/<uuid:cart_id>/", views.CartViewSet.as_view({"get": "retrieve"})),
    path("products/<int:pk>/reviews/", views.ReviewViewSet.as_view({"post": "create"})),
    # Include the nested cart items router
    path("", include(cart_router.urls)),
]
