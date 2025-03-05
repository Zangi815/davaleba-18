from django.urls import path, include
from rest_framework_nested import routers
from products.views import ProductViewSet, ReviewViewSet, FavoriteProductViewSet, CartViewSet,ProductImageViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)

product_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)
product_router.register('images', ProductImageViewSet, basename='product-images')

review_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)
review_router.register('reviews', ReviewViewSet, basename='product-reviews')

favorite_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)
favorite_router.register('favorite_products', FavoriteProductViewSet, basename='product-favorite-products')

cart_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)
cart_router.register('cart', CartViewSet, basename='product-cart')

tag_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(review_router.urls)),
    path('', include(favorite_router.urls)),
    path('', include(cart_router.urls)),
    path('', include(tag_router.urls)),
]
