from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views

router = SimpleRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet, basename="collections")

urlpatterns = [
    path("", include(router.urls)),
    # Add a URL pattern for the collection detail view
    path(
        "collections/<int:pk>/",
        views.CollectionViewSet.as_view({"get": "retrieve"}),
        name="collection-detail",
    ),
]
