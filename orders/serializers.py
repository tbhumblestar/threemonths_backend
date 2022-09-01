from django.db             import transaction
from rest_framework        import serializers
from drf_spectacular.utils import extend_schema_serializer

from .models        import (
                        Order,
                        PackageOrder,
                        OrderedProduct,
                        CafeOrder,
                        CakeOrder,
                        Review
)
from products.models import Product


#PackageOrder
class OrderedProductSerializer(serializers.ModelSerializer):
    #primary_key로 설정된 필드는 언제나 read_only=True임
    #따라서, read_only=False를 해주지 않으면,  is_valid()를 통한 유효성 검사과정에서 해당 필드가 아예 삭제되어, 해당 필드의 데이터도 사라져버림
    product_id   = serializers.IntegerField(read_only=False)
    product_name = serializers.CharField(source='product.product_name',read_only=True)
    
    class Meta:
        model  = OrderedProduct
        fields = ["product_id","buying","product_name"]


class PackageOrderSerializer(serializers.ModelSerializer):
    orderedproducts = OrderedProductSerializer(many=True)
    
    class Meta:
        model  = PackageOrder
        fields = [
            "id","delivery_location","delivery_date","is_packaging","purpose",
            "orderedproducts"
        ]     
    
    @transaction.atomic
    def create(self,validated_data):
        orderedproducts = validated_data.pop('orderedproducts')
        packageorder = PackageOrder.objects.create(**validated_data)        
        
        for products_data in orderedproducts:
            OrderedProduct.objects.create(package_order=packageorder,**products_data)
        return packageorder

    @transaction.atomic
    def update(self,instance,validated_data):
        instance.delivery_location = validated_data.get('delivery_location',instance.delivery_location)
        instance.delivery_date     = validated_data.get('delivery_date',instance.delivery_date)
        instance.is_packaging      = validated_data.get('is_packaging',instance.is_packaging)
        instance.purpose           = validated_data.get('purpose',instance.purpose)
        
        instance.save()
        
        
        orderedproducts = validated_data.pop('orderedproducts',None)
        
        if orderedproducts:
            
            existing_products_id_set =  set(OrderedProduct.objects.filter(package_order=instance).values_list('product_id',flat=True))
            
            new_products_id_set = set()
            for products_data in orderedproducts:
                new_products_id_set.add(products_data['product_id'])
            
            
            
            
            delete_id_set = existing_products_id_set - new_products_id_set
            OrderedProduct.objects.filter(package_order=instance,product_id__in=delete_id_set).delete()
            
            add_id_set = new_products_id_set - existing_products_id_set
            for id in add_id_set:
                OrderedProduct.objects.create(
                    package_order = instance,
                    product_id    = id,
                    buying        = True
                )
            
        return instance
    
    def to_representation(self, instance):
        
        ret = super().to_representation(instance)
        
        if self.context.get('detail'):
            products = Product.objects.filter(is_active=True,category='bread')
            
            orderedproducts_id_list = list(OrderedProduct.objects.filter(package_order=instance).values_list('product_id',flat=True))
            
            products = [
                {
                    "product_id"   : product.id,
                    "buying"       : True if product.id in orderedproducts_id_list else False,
                    "product_name" : product.product_name,
                } for product in products
            ]
            
            ret['orderedproducts'] = products
            
        return ret

class CafeOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = CafeOrder
        fields = ['id','cafename','cafe_owner_name','corporate_registration_num','cafe_location','product_explanation']


class CakeOrderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(read_only=False)
    product_name = serializers.CharField(source='product.product_name',read_only=True)
    
    class Meta:
        model  = CakeOrder
        fields = [
            "id","product_id","product_name","want_pick_up_date","count"
            ]

@extend_schema_serializer(exclude_fields=None)
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
        
    #없는 필드 제거. 굳이 list_serializer필드를 만들지 않아도 됨
    def to_representation(self, instance,*args,**kwargs):
        
        ret      = super().to_representation(instance)
        
        type_set = set(['package','cake','cafe'])
        type_set.remove(ret['type'])
        
        for order_type in type_set:
            ret.pop(f"{order_type}orders")

        #for detail check   
        if 'is_staff' in self.context:
            ret['is_staff'] = self.context.get('is_staff')

        return ret
    
class UserOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Order
        fields = ['id','type','title','created_at']
        
        
class ReviewSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_nickname = serializers.SerializerMethodField()
    
    def get_user_nickname(self,object):
        return object.user.nickname
    
    class Meta:
        model  = Review
        fields = [
            'id','content','order','created_at','updated_at','img_url','img_s3_path',
            'user','user_nickname',
            ]