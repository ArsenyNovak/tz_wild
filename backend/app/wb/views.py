from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        min_rating = self.request.GET.get('min_rating')
        min_comment = self.request.GET.get('min_comment')

        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                raise ValidationError({'min_price': 'Должно быть числом.'})
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                raise ValidationError({'max_price': 'Должно быть числом.'})
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=float(min_rating))
            except ValueError:
                raise ValidationError({'min_rating': 'Должно быть числом.'})
        if min_comment:
            try:
                queryset = queryset.filter(count_comment__gte=float(min_comment))
            except ValueError:
                raise ValidationError({'min_comment': 'Должно быть числом.'})

        return queryset
