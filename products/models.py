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
    is_active            = models.BooleanField(default=True)
    tag                  = models.CharField(default=None,null=True,blank=True,max_length=50)
    sellout              = models.BooleanField(default=False)

    
    def __str__(self):
        return str(self.id) + " | " + self.product_name +  "|" + " 가격 : " + str(self.price)

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
    
    product     = models.ForeignKey("Product",on_delete=models.CASCADE,related_name='product_images')
    img_src     = models.CharField(max_length=250)
    page        = models.CharField(max_length=50)
    place       = models.CharField(max_length=50)
    description = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.product.product_name
    
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


class Package(models.Model):
    description  = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'package'
        

class PackageImage(models.Model):
    
    package   = models.ForeignKey("Package",on_delete=models.CASCADE)
    img_src = models.CharField(max_length=250)
    page      = models.CharField(max_length=50)
    place     = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'package_images'