from turtle import title
from django.db           import models
from core.models         import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(TimeStampedModel):
    order_type = (
        ('cafe','Cafe order'),
        ('package','Package order'),
        ('cake','Cake order')
    )

    status_type = (
        ('not_confirmed','not_confirmed'),
        ('confirmed','confirmed'),
        ("can't_cancel","can't_cancel"),
        ('completed','completed')
    )

    user                   = models.ForeignKey(User,on_delete=models.PROTECT)
    title                  = models.CharField(max_length=100)
    type                   = models.CharField(max_length=100, choices=order_type)
    customer_name          = models.CharField(max_length=50)
    contact                = models.CharField(max_length=50)
    status                 = models.CharField(max_length=50, choices= status_type, default='not_confirmed')
    additional_explanation = models.CharField(max_length=300, null=True,blank=True)
    
    class Meta:
        db_table = 'orders'
        

class PackageOrder(TimeStampedModel):
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    delivery_location = models.CharField(max_length=100)
    delivery_date = models.DateField()
    is_packaging = models.CharField(max_length=100, blank=True,null=True)
    
    class Meta:
        db_table = 'package_orders'


class OrderedProductsInPackage(TimeStampedModel):
    order_package = models.ForeignKey('PackageOrder',on_delete=models.CASCADE)
    product       = models.ForeignKey('products.Product',on_delete=models.CASCADE)
    count         = models.BigIntegerField()
    
    class Meta:
        db_table = 'ordered_products_in_packages'


class CafeOrder(TimeStampedModel):
    order               = models.ForeignKey('Order',on_delete=models.CASCADE)
    cafename            = models.CharField(max_length=50)
    cafe_owner_name     = models.CharField(max_length=50)
    cafe_location       = models.CharField(max_length=50)
    product_explanation = models.TextField(blank=True,null=True)
    
    class Meta:
        db_table = 'cafe_orders'
    

class CakeOrder(TimeStampedModel):
    order             = models.ForeignKey('Order',on_delete=models.CASCADE)
    want_pick_up_date = models.DateField()
    
    class Meta:
        db_table = 'cake_orders'


class OrderedCake(TimeStampedModel):
    product = models.ForeignKey('products.Product',on_delete=models.CASCADE)
    count   = models.BigIntegerField()
    
    class Meta:
        db_table = 'ordered_cakes'