from rest_framework import serializers
from .models        import Order,PackageOrder,OrderedProduct, CafeOrder, CakeOrder

#PackageOrder
class OrderedProductSerializer(serializers.ModelSerializer):
    #primary_key로 설정된 필드는 언제나 read_only=True임
    #따라서, read_only=False를 해주지 않으면,  is_valid()를 통한 유효성 검사과정에서 해당 필드가 아예 삭제되어, 해당 필드의 데이터도 사라져버림
    product_id = serializers.IntegerField(read_only=False)
    product_name = serializers.CharField(source='product.product_name',read_only=True)
        
    class Meta:
        model  = OrderedProduct
        fields = ["product_id","count","product_name"]


class PackageOrderSerializer(serializers.ModelSerializer):
    orderedproducts = OrderedProductSerializer(many=True)
    
    class Meta:
        model  = PackageOrder
        fields = [
            "id","delivery_location","delivery_date","is_packaging",
            "orderedproducts"
        ]     
    
    def create(self,validated_data):
        orderedproducts = validated_data.pop('orderedproducts')
        packageorder = PackageOrder.objects.create(**validated_data)
        # print("self.context : ",self.context)
        
        
        for products_data in orderedproducts:
            OrderedProduct.objects.create(package_order=packageorder,**products_data)
        return packageorder


#Cafe Order
class CafeOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = CafeOrder
        fields = ['id','cafename','cafe_owner_name','corporate_registration_num','cafe_location']

#Cake Order
class CakeOrderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(read_only=False)
    product_name = serializers.CharField(source='product.product_name',read_only=True)
    
    class Meta:
        model  = CakeOrder
        fields = [
            "id","product_id","product_name","want_pick_up_date","count"
            ]

    def create(self,validated_data):
        cakeorder = CakeOrder.objects.create(**validated_data)
            
        return cakeorder




class OrderSerializer(serializers.ModelSerializer):
    """
        order_main_serializer
    """
    packageorders = PackageOrderSerializer(read_only=True)
    cafeorders    = CafeOrderSerializer(read_only=True)
    cakeorders    = CakeOrderSerializer(read_only=True)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        want_fields = self.context.get('want_fields')
        
        if want_fields:
            allowed = set(want_fields)
            existing = set(self.fields)
            for field_name in existing-allowed:
                self.fields.pop(field_name)
        

    class Meta:
        model  = Order
        fields = [
            'id','type','title','customer_name','contact','status','additional_explanation',"created_at","updated_at",
            'packageorders','cafeorders','cakeorders'
        ]
        
    #없는 필드 제거    
    def to_representation(self, instance,*args,**kwargs):
        ret= super().to_representation(instance)
        
        if ret['packageorders'] == None:
            ret.pop('packageorders')
            
        if ret['cakeorders'] == None:
            ret.pop('cakeorders')
        
        if ret['cafeorders'] == None:
            ret.pop('cafeorders')
            
        return ret