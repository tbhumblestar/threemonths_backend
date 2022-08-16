from unicodedata import name
from rest_framework.test  import APITestCase
from rest_framework       import status
from django.urls          import reverse
from products.models      import Product
from orders.models        import Order, PackageOrder, OrderedProduct, CakeOrder, CafeOrder
from django.contrib.auth  import get_user_model
from datetime             import datetime,timedelta
from freezegun            import freeze_time
import json

User = get_user_model()

@freeze_time("2022-08-16")
class OrderCreateListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        
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
        cls.user = User.objects.create(
            id                = 1,
            nickname          = 'test_nickname',
            email             = 'test_email@test.com',
            login_type        = "KakaoLogin",
            profile_image_url = 'test_profile_image_url@test.com',
            kakao_id          = 11
        )
        
        cls.admin_user = User.objects.create(
            id                = 2,
            nickname          = 'test_admin_nickname',
            email             = 'test_admin_email@test.com',
            login_type        = "KakaoLogin",
            profile_image_url = 'test_admin_profile_image_url@test.com',
            kakao_id          = 12,
            is_staff          = True
        )
        
        #packagae:order
        cls.order_package = Order.objects.create(
            user                   = cls.user,
            id                     = 1,
            title                  = "test_order_package",
            type                   = "package",
            customer_name          = "test_customer",
            contact                = "000-0000-0000",
            additional_explanation = "test_explanation",
        )
        cls.packageorder = PackageOrder.objects.create(
            id                = 1 ,
            order             = cls.order_package,
            delivery_location = 'test_location',
            delivery_date     = datetime.now() + timedelta(days=5),
            is_packaging      = "test_packaging",
            purpose           = "_test"
        )
        OrderedProduct.objects.bulk_create(
            [
                OrderedProduct(
                    id            = 1,
                    package_order = cls.packageorder,
                    product_id    = 1,
                    buying        = True
                ),
                OrderedProduct(
                    id            = 2,
                    package_order = cls.packageorder,
                    product_id    = 2,
                    buying        = True
                ),
            ]
        )
        
        #packagae:cafe
        cls.order_cafe = Order.objects.create(
            user                   = cls.user,
            id                     = 2,
            title                  = "test_order_cafe",
            type                   = "cafe",
            customer_name          = "test_customer",
            contact                = "000-0000-0000",
            additional_explanation = "test_explanation",
        )
        cls.cafeorder = CafeOrder.objects.create(
            id                         = 1 ,
            order                      = cls.order_cafe,
            cafename                   = 'test_cafename',
            cafe_owner_name            = 'test_owner',
            corporate_registration_num = "test_regi_num",
            cafe_location              = "test_location",
            product_explanation        = "test_product_explanation"
        )
        
        #packagae:cake
        cls.order_cake = Order.objects.create(
            user                   = cls.user,
            id                     = 3,
            title                  = "test_order_cake",
            type                   = "cake",
            customer_name          ="test_customer",
            contact                = "000-0000-0000",
            additional_explanation = "test_explanation",
        )
        cls.packageorder = CakeOrder.objects.create(
            id                = 1 ,
            order             = cls.order_cake,
            want_pick_up_date = datetime.now() + timedelta(days=5),
            product_id        = 3,
            count             = 1
        )
        
        
        
    def test_list_order(self):
        pass
        # #for checking
        # print("order_users : ",User.objects.all().values_list('id'))
        # print("order_products : ",Product.objects.all())
        # print("orders : ",Order.objects.all().values())
        # print("package_orders_first_packageorders : ",Order.objects.all().first().packageorders)
        # print("PackageOrder : ",PackageOrder.objects.all().values())
        # print("PackageOrder_first_orderedproducts : ",PackageOrder.objects.first().orderedproducts.all())
        # print("OrderedProducts : ",OrderedProduct.objects.all().values())
        # print("CakeOrder : ",CakeOrder.objects.all().values())
        # print("CafeOrder : ",CafeOrder.objects.all().values())
    
    def test_list_order_type_package_order(self):
        
        data = [{
            'id'                    : 1,
            'type'                  : 'package',
            'title'                 : 'test_order_package',
            'customer_name'         : 'test_customer',
            'contact'               : '000-0000-0000',
            'status'                : 'not_confirmed',
            'additional_explanation': 'test_explanation',
            'created_at'            : '2022-08-16T00:00:00',
            'updated_at'            : '2022-08-16T00:00:00',
            'packageorders': {
                'id'               : 1,
                'delivery_location': 'test_location',
                'delivery_date'    : (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                'is_packaging'     : 'test_packaging',
                'purpose'          : '_test',
                'orderedproducts'  : [
                    {
                        'product_id'  : 1,
                        'buying'      : True,
                        'product_name': 'test_product1'},
                    {
                        'product_id'  : 2,
                        'buying'      : True, 
                        'product_name': 'test_product2'}
                    ]
                }
            }]
        
        response = self.client.get('/orders/?type=package')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,data)
    
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