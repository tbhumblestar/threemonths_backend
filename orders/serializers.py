from rest_framework import serializers
from .models        import Order,PackageOrder,OrderedProductsInPackage



class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        exclude = ['user']