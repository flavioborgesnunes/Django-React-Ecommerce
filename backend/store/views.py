from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from store.models import (Cart, CartOrder, CartOrderItem, Category, Color,
                          Coupon, Gallery, Notification, Product, ProductFaq,
                          Review, Size, Specification, Wishlist)
from store.serializers import (CartOrderItemSerializer, CartOrderSerializer,
                               CartSerializer, CategorySerializer,
                               ProductSerializer)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return Product.objects.get(slug=slug)


class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_class = [AllowAny]
