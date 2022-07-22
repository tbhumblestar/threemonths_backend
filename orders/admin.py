from django.contrib import admin
from .models        import *

admin.site.register(Order)

admin.site.register(PackageOrder)
admin.site.register(OrderedProductsInPackage)

admin.site.register(CafeOrder)

admin.site.register(CakeOrder)
admin.site.register(OrderedCake)