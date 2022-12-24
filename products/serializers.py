from rest_framework import serializers
from .models        import (
                        IndependentImage,
                        Product, 
                        ProductImage    
)


class IndependentImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = IndependentImage
        fields = ['id','img_src','description']


#List serializer 데이터 하나하나에 적용됨
#print("a")를 중간에 끼워넣으면 쿼리셋만큼 a가 출력됨
# class FilteredProductImageSerializer(serializers.ListSerializer):

#     def to_representation(self, data,*args,**kwargs):

#         #참고) 다음과 같이 상위 시리얼라이저의 context에 접근도 가능하다
#         # print("self.parent.context : ",self.parent.context)
        
#         img_filter = self.child.context.get('img_filter')
#         if img_filter:
#             data = data.filter(**img_filter)
        
#         #super은 하위클래스와 self를 인자로 받음. 그러나 생략해줘도 됨
#             #super().to_representation = super(ListSerializer,self).to_representation
#         #super를 통해 호출된 상위 클래스의 메서드는 메서드함수처럼 self를 인자로 받지 않음
#         return super(FilteredProductImageSerializer,self).to_representation(data)
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductImage
        fields ='__all__'

        #list serializer를 커스터마이징 해주려면, 새로운 serializer를 생성해서 커스터마이징 해준 후 적용시켜야 함
        #만약 그렇게 하지 않고 그냥 이 serializer를 아무리 커스터마이징해줘봤자, list가 아니라 그냥 instance를 받는 serializer를 커스터마이징해주는 것임
        # list_serializer_class = FilteredProductImageSerializer


class ProductSerializer(serializers.ModelSerializer):
        
    product_images = ProductImageSerializer(many=True,read_only=True)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        want_fields = self.context.get('want_fields')
        
        if want_fields:
            allowed = set(want_fields)
            existing = set(self.fields)
            for field_name in existing-allowed:
                self.fields.pop(field_name)


    class Meta:
        model = Product
        fields = ['id',
                'product_name',
                'category',
                'price',
                'description',
                'optional_description',
                'product_images',
                'is_active',
                ]