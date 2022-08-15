from rest_framework.test  import APITestCase
from rest_framework       import status
from django.urls          import reverse
from products.models      import Product
from orders.models        import Order
from django.contrib.auth  import get_user_model

import json

User = get_user_model()


# class OrderCreateListTestCase(APITestCase):
#     def setUp(self):
        
#         #Product
#         setup_product_list = [
#             Product(
#                 id                   = 1,
#                 category             = 'bread',
#                 product_name         = 'test_product1',
#                 price                = 10000,
#                 optional_description = 'test_optional_description1',
#                 description          = 'test_description',
#                 is_active            = True,
#                 tag                  = None,
#                 sellout              = False,
#             ),
#             Product(
#                 id                   = 2,
#                 category             = 'bread',
#                 product_name         = 'test_product2',
#                 price                = 10000,
#                 optional_description = 'test_optional_description2',
#                 description          = 'test_description',
#                 is_active            = True,
#                 tag                  = None,
#                 sellout              = False,
#             ),
#             Product(
#                 id                   = 3,
#                 category             = 'cake',
#                 product_name         = 'test_product3',
#                 price                = 10000,
#                 optional_description = 'test_optional_description3',
#                 description          = 'test_description',
#                 is_active            = True,
#                 tag                  = None,
#                 sellout              = False,
#             ),
#         ]        
        
#         Product.objects.bulk_create(setup_product_list)
        
#         #user
#         self.user = User.objects.create(
#             id                = 1,
#             nickname          = 'test_nickname',
#             email             = 'test_email@test.com',
#             login_type        = "KakaoLogin",
#             profile_image_url = 'test_profile_image_url@test.com',
#             kakao_id          = 10
#         )
        
#         self.user.set_unusable_password()
#         self.user.save()
        
#         #order
        
#         Order.objects.create
        
#     def test_list_order(self):
#         pass
    
#     def test_list_order_type_package_order(self):
#         pass
    
#     def test_create_package_order_auth_success(self):
#         pass
    
#     def test_create_package_order_unauth_fail(self):
#         pass
