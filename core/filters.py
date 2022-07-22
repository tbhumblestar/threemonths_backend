from django_filters import rest_framework as filters

from products.models import IndependentImage, Product

class IndependentImageFilter(filters.FilterSet):
    class Meta:
        model = IndependentImage
        fields = {
            'page':['exact'],
            'place':['exact']
        }
        
class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'category':['exact']
        }
