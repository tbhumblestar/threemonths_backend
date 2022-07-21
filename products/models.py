from django.db import models


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
    signature            = models.BooleanField(default = False)
    sellout              = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'


class Ingredient(models.Model):
    
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    name    = models.CharField(max_length=50)
    origin  = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'ingredients'


class ProductImage(models.Model):
    
    page_category =(
        ('main','main'),
        ('detail','detail')
    )
    
    product   = models.ForeignKey("Product",on_delete=models.CASCADE)
    image_url = models.CharField(max_length=250)
    page      = models.CharField(max_length=50)
    place     = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'product_images'
        

class IndependentImage(models.Model):
    image_url = models.CharField(max_length=250)
    page      = models.CharField(max_length=50)
    place     = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'independent_images'


class Package(models.Model):
    description  = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'package'
        

class PackageImage(models.Model):
    
    package   = models.ForeignKey("Package",on_delete=models.CASCADE)
    image_url = models.CharField(max_length=250)
    page      = models.CharField(max_length=50)
    place     = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'package_images'