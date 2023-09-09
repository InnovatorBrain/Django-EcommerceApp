from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
#Parent router
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet, basename="collections")
#Child router
products_router =routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    # Add a URL pattern for the collection detail view
    path('collections/<int:pk>/', views.CollectionViewSet.as_view({'get': 'retrieve'}), name='collection-detail')
]


