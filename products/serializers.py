from rest_framework import serializers
from .models        import IndependentImage, Product, ProductImage

class IndependentImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IndependentImage
        fields = ['img_src','description']



#List serializer 데이터 하나하나에 적용됨
#print("a")를 중간에 끼워넣으면 쿼리셋만큼 a가 출력됨
class FilteredProductImageSerializer(serializers.ListSerializer):

    def to_representation(self, data,*args,**kwargs):

        #참고) 다음과 같이 상위 시리얼라이저의 context에 접근도 가능하다
        # print("self.parent.context : ",self.parent.context)
        
        
        print("child_self.context : ",self.context)
        img_filter = self.context['img_filter']
        print(img_filter)
        if self.context:
            data = data.filter(**img_filter)
        
        #super은 하위클래스와 self를 인자로 받음. 그러나 생략해줘도 됨
            #super().to_representation = super(ListSerializer,self).to_representation
        #super를 통해 호출된 상위 클래스의 메서드는 메서드함수처럼 self를 인자로 받지 않음
        return super(FilteredProductImageSerializer,self).to_representation(data)
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields ='__all__'

        #list serializer를 커스터마이징 해주려면, 아예 다른 친구를 가져와야 함. 아래 설정철머 다른 serializer로 아예 바뀌어버리기 때문바뀌기 때문
        #따라서 아래 설정된 list serializer가 아니라, 그냥 이 serializer를 아무리 커스터마이징해줘봤자, list가 아니라 그냥 instance를 받는 serializer를 커스터마이징해주는 것임
        list_serializer_class = FilteredProductImageSerializer
    


class ProductSerializer(serializers.ModelSerializer):
    
    # main_list_img_src = serializers.SerializerMethodField()
    # def get_main_list_img_src(self,object):
    #     return object.productimage_set.get(page='main',place='list').img_src
    
    productimage_set = ProductImageSerializer(many=True,read_only=True)
    
    def __init__(self,*args,**kwargs):
        
        self.additional_context = kwargs.pop('additional_context',{})
        self.want_fields        = self.additional_context.get('want_fields',{})
        self.img_filter         = self.additional_context.get('img_filter',{})
            
        super().__init__(*args,**kwargs)
        
        print("self.context : ",self.context)
        print("self.fields[productimage_set].context : ",self.fields['productimage_set'].context)
        print("self.fields[productimage_set].context type :",type(self.fields['productimage_set'].context))
        
        
        self.fields['productimage_set'].context.update({"img_filter":self.img_filter})

        print("updated!")
        
        print("self.fields[productimage_set].context :",self.fields['productimage_set'].context)
                
    class Meta:
        model = Product
        fields = ['id',
                'product_name',
                'price',
                'description',
                'optional_description',
                'productimage_set',
                # 'main_list_img_src'
                ]
        
        

#동적 필터링
#list serializer 커스터마이징(get_initial > to_representation)
#Serializer Method Field
