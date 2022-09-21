from django.contrib  import admin
from products.models import *
# Register your models here.

#Product
admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(ProductImage)

#IndependentImage
admin.site.register(IndependentImage)