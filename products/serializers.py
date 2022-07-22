from rest_framework import serializers
from .models        import IndependentImage, Product, ProductImage

class IndependentImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IndependentImage
        fields = ['img_src','description']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields ='__all__'

class ProductSerializer(serializers.ModelSerializer):
    
    productimage_set = ProductImageSerializer(many=True,read_only=True)
    
    class Meta:
        model = Product
        fields = ['id','product_name','price','description','optional_description','productimage_set']
        

