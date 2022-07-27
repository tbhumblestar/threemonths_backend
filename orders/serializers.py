from rest_framework import serializers
from .models        import Order,PackageOrder,OrderedProduct, CafeOrder, CakeOrder, OrderedCake

class OrderedProductSerializer(serializers.ModelSerializer):
    
    product_name = serializers.CharField(source='product.product_name',read_only=True)
    
    class Meta:
        model  = OrderedProduct
        fields = [
            "product_id","count","product_name"
        ]
        

class PackageOrderSerializer(serializers.ModelSerializer):
    orderedproducts = OrderedProductSerializer(many=True,read_only=True)
    
    class Meta:
        model  = PackageOrder
        fields = [
            "id","delivery_location","delivery_date","is_packaging",
            "orderedproducts"
        ]     
    
    def create(self,validated_data):
        print("validated_data : ",validated_data)
        packageorder = PackageOrder.objects.create(**validated_data)
        print("self.context : ",self.context)
        
        
        for products_data in self.context.get('orderedproducts'):
            OrderedProduct.objects.create(package_order=packageorder,**products_data)
            
        return packageorder

class CafeOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = CafeOrder
        fields = '__all__'
        
class OrderedCakeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = OrderedCake
        fields = "__all__"
        
class CakeOrderSerializer(serializers.ModelSerializer):
    orderedcakes = OrderedCakeSerializer(read_only=True,many=True)
    
    class Meta:
        model  = CakeOrder
        fields = [
            "want_pick_up_date","orderedcakes"
        ]

class OrderSerializer(serializers.ModelSerializer):
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