from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls





# MY PREVIOUS
# urlpatterns = [
#     path("", include(router.urls)),
#     # Add a URL pattern for the collection detail view
#     path(
#         "collections/<int:pk>/",
#         views.CollectionViewSet.as_view({"get": "retrieve"}),
#         name="collection-detail",
#     ),
#     path("carts/<uuid:cart_id>/", views.CartViewSet.as_view({"get": "retrieve"})),
#     path("products/<int:pk>/reviews/", views.ReviewViewSet.as_view({"post": "create"})),
#     # Include the nested cart items router
#     path("", include(cart_router.urls)),
# ]
