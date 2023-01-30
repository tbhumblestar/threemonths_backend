from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache


class Product(models.Model):
    
    product_category = (
        ('bread','bread'),
        ('cake','cake')
    )
    
    category             = models.CharField(max_length=30,choices=product_category)
    product_name         = models.CharField(max_length=50)
    price                = models.PositiveIntegerField()
    description          = models.CharField(max_length=300,null=True,blank=True)
    optional_description = models.CharField(max_length=300,null=True,blank=True)
    is_active            = models.BooleanField(default=True)
    tag                  = models.CharField(default=None,null=True,blank=True,max_length=50)
    sellout              = models.BooleanField(default=False)

    
    def __str__(self):
        return str(self.id) + " | " + self.product_name +  " | " + " 가격 : " + str(self.price)

    class Meta:
        db_table = 'products'

@receiver(post_delete, sender=Product)
def product_post_delete_handler(sender, **kwargs):
    cache.delete('product_list_all_user')


@receiver(post_save, sender=Product)
def product_post_save_handler(sender, **kwargs):
    cache.delete('product_list_all_user')


class ProductImage(models.Model):
    
    product     = models.ForeignKey("Product",on_delete=models.CASCADE,related_name='product_images')
    img_url     = models.CharField(max_length=500)
    s3_path     = models.CharField(max_length=500)
    property    = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.property} page | {self.product.product_name}"
    
    class Meta:
        db_table = 'product_images'
        

class IndependentImage(models.Model):
    img_src     = models.CharField(max_length=250)
    page        = models.CharField(max_length=50)
    place       = models.CharField(max_length=50)
    description = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.description
    
    class Meta:
        db_table = 'independent_images'