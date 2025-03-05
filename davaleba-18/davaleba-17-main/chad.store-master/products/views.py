from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from products.filters import ProductFilter
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from products.models import (
    Product,
    Review,
    FavoriteProduct,
    Cart, ProductTag, ProductImage
)
from products.serializers import (
    ProductSerializer,
    ReviewSerializer,
    FavoriteProductSerializer,
    CartSerializer,
    ProductTagSerializer, ProductImageSerializer
    )


class ProductViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     CreateModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['price', 'categories']
    filterset_class = ProductFilter


class ReviewViewSet(ListModelMixin,
                    CreateModelMixin,
                    GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self,instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can't delete this review")
        instance.delete()

    def perform_destroy(self,serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You can't change this review")
        serializer.save()


    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])


class FavoriteProductViewSet(ListModelMixin,
                             RetrieveModelMixin,
                             CreateModelMixin,
                             DestroyModelMixin,
                             GenericViewSet):
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)


class CartViewSet(ListModelMixin,
                  CreateModelMixin,
                  UpdateModelMixin,
                  GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class ProductTagViewSet(ListModelMixin,
                        GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]


class ProductImageViewSet(ListModelMixin,
                          RetrieveModelMixin,
                          CreateModelMixin,
                          DestroyModelMixin,
                          GenericViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductImage.objects.filter(product__id=self.kwargs['product_id'])
