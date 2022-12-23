from django_filters import rest_framework as filters

from products.models import IndependentImage, Product
from orders.models import Order, Review


class IndependentImageFilter(filters.FilterSet):
    class Meta:
        model = IndependentImage
        fields = {"page": ["exact"], "place": ["exact"]}


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {"category": ["exact"]}


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {"type": ["exact"]}


class ReviewFilter(filters.FilterSet):
    class Meta:
        model = Review
        fields = {"order__type": ["iexact"]}
