from rest_framework import serializers
from .models        import IndependentImage, Product, ProductImage

class IndependentImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IndependentImage
        fields = ['img_src','description']


class FilteredProductImageSerializer(serializers.ListSerializer):
    def to_representation(self, data,*args,**kwargs):
        print(kwargs)
        return super().to_representation(*args,**kwargs)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields ='__all__'
        # list_serializer_class = FilteredProductImageSerializer


class ProductSerializer(serializers.ModelSerializer):
    
    main_list_img_src = serializers.SerializerMethodField()
    def get_main_list_img_src(self,object):
        return object.productimage_set.get(page='main',place='list').img_src
    
    # productimage_set = ProductImageSerializer(many=True,read_only=True)
    
    # def __init__(self,*args,**kwargs):
        
    #     print("kwargs",kwargs)
    #     self.image_parameter = kwargs.pop('image_parameter',None)
        
    #     super().__init__(*args,**kwargs)
    #     print("self.context :",self.context)
    #     print("self.fields[productimage_set] :",self.fields['productimage_set'])
    #     print("self.fields[productimage_set]'s type :",type(self.fields['productimage_set'].context))
        
    #     self.fields['productimage_set'].context.update(self.context)
        
    #     print("updated!")
    #     print("self.fields[productimage_set] :",self.fields['productimage_set'])
        
        
        
    class Meta:
        model = Product
        fields = ['id',
                'product_name',
                'price',
                'description',
                'optional_description',
                # 'productimage_set',
                'main_list_img_src'
                ]
        
        

#동적 필터링
#list serializer 커스터마이징(get_initial > to_representation)
#Serializer Method Field
