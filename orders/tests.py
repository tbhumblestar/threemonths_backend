from unicodedata import name
from rest_framework.test  import APITestCase
from rest_framework       import status
from django.urls          import reverse
from products.models      import Product
from orders.models        import Order, PackageOrder, OrderedProduct, CakeOrder, CafeOrder
from django.contrib.auth  import get_user_model
from datetime             import datetime,timedelta

import json

User = get_user_model()


class OrderCreateListTestCase(APITestCase):
    # @classmethod
    # def setUpTestData(cls):
    
    def setUp(self):

        
        #Product
        setup_product_list = [
            Product(
                id                   = 1,
                category             = 'bread',
                product_name         = 'test_product1',
                price                = 10000,
                optional_description = 'test_optional_description1',
                description          = 'test_description',
                is_active            = True,
                tag                  = None,
                sellout              = False,
            ),
            Product(
                id                   = 2,
                category             = 'bread',
                product_name         = 'test_product2',
                price                = 10000,
                optional_description = 'test_optional_description2',
                description          = 'test_description',
                is_active            = True,
                tag                  = None,
                sellout              = False,
            ),
            Product(
                id                   = 3,
                category             = 'cake',
                product_name         = 'test_product3',
                price                = 10000,
                optional_description = 'test_optional_description3',
                description          = 'test_description',
                is_active            = True,
                tag                  = None,
                sellout              = False,
            ),
        ]        
        
        Product.objects.bulk_create(setup_product_list)
        
        #user
        self.user = User.objects.create(
            id                = 1,
            nickname          = 'test_nickname',
            email             = 'test_email@test.com',
            login_type        = "KakaoLogin",
            profile_image_url = 'test_profile_image_url@test.com',
            kakao_id          = 11
        )
        
        self.admin_user = User.objects.create(
            id                = 2,
            nickname          = 'test_admin_nickname',
            email             = 'test_admin_email@test.com',
            login_type        = "KakaoLogin",
            profile_image_url = 'test_admin_profile_image_url@test.com',
            kakao_id          = 12,
            is_staff          = True
        )
        
        #packagae:order
        self.order_package = Order.objects.create(
            user = self.user,
            id = 1,
            title = "test_order_package",
            type = "package",
            customer_name ="test_customer",
            contact = "000-0000-0000",
            additional_explanation = "test_explanation"
        )
        self.packageorder = PackageOrder.objects.create(
            id = 1 ,
            order = self.order_package,
            delivery_location = 'test_location',
            delivery_date = datetime.now() + timedelta(days=5),
            is_packaging = "test_packaging",
            purpose = "_test"
        )
        OrderedProduct.objects.bulk_create(
            [
                OrderedProduct(
                    id=1,
                    package_order = self.packageorder,
                    product_id = 1,
                    buying = True
                ),
                OrderedProduct(
                    id=2,
                    package_order = self.packageorder,
                    product_id = 2,
                    buying = True
                ),
            ]
        )
        
        #packagae:order
        self.order_package = Order.objects.create(
            user = self.user,
            id = 1,
            title = "test_order_package",
            type = "package",
            customer_name ="test_customer",
            contact = "000-0000-0000",
            additional_explanation = "test_explanation"
        )
        self.packageorder = PackageOrder.objects.create(
            id = 1 ,
            order = self.order_package,
            delivery_location = 'test_location',
            delivery_date = datetime.now() + timedelta(days=5),
            is_packaging = "test_packaging",
            purpose = "_test"
        )
        
        #packagae:order
        self.order_package = Order.objects.create(
            user = self.user,
            id = 1,
            title = "test_order_package",
            type = "package",
            customer_name ="test_customer",
            contact = "000-0000-0000",
            additional_explanation = "test_explanation"
        )
        self.packageorder = PackageOrder.objects.create(
            id = 1 ,
            order = self.order_package,
            delivery_location = 'test_location',
            delivery_date = datetime.now() + timedelta(days=5),
            is_packaging = "test_packaging",
            purpose = "_test"
        )
        
        
        
    def test_list_order(self):
        
        # #for checking
        # print("test_list_order_users : ",User.objects.all().values_list('id'))
        # print("test_list_order_products : ",Product.objects.all())
        # print("test_list_orders : ",Order.objects.all().values())
        # print("test_list_orders_first_packageorders : ",Order.objects.all().first().packageorders)
        # print("test_list_PackageOrder : ",PackageOrder.objects.all().values())
        # print("test_list_PackageOrder_first_orderedproducts : ",PackageOrder.objects.first().orderedproducts.all())
        # print("test_list_OrderedProducts : ",OrderedProduct.objects.all().values())
    
    def test_list_order_type_package_order(self):
        pass
    
    def test_create_package_order(self):
        pass
    
    def test_create_package_order_fail_by_permission(self):
        pass

# class OrderDetailTestCase(APITestCase):

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
        
#         self.admin_user = User.objects.create(
#             id                = 2,
#             nickname          = 'test_admin_nickname',
#             email             = 'test_admin_email@test.com',
#             login_type        = "KakaoLogin",
#             profile_image_url = 'test_admin_profile_image_url@test.com',
#             kakao_id          = 12,
#             is_staff          = True
#         )

#         #order
#     def teardown(self):
#         self.client.force_authenticate(user=None)
        
#     def test_retrieve_order(self):
#         pass
    
#     def test_retrieve_order_fail_by_permission(self):
#         pass