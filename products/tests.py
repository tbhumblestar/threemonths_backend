from rest_framework.test import APITestCase
from rest_framework      import status
from django.urls         import reverse
import json

from products.models import IndependentImage, Product, ProductImage

class IndependentImageListTestCase(APITestCase):
    def setUp(self):
        setup_indenpendent_image_list = [
            IndependentImage(
                id      = 1,
                img_src = 'test1@test.com1',
                page    = 'test_page1',
                place   = 'test_place1',
                description = 'test_description1'
            ),
            IndependentImage(
                id      = 2,
                img_src = 'test@test.com2',
                page    = 'test_page2',
                place   = 'test_place2',
                description = 'test_description2'
            )
        ]
        
        IndependentImage.objects.bulk_create(
            setup_indenpendent_image_list
        )
    
    def test_list_independent_images_success(self):
        
        data = [
            {
            'id'          : 1,
            'img_src'     : 'test1@test.com1',
            'description' : 'test_description1',
        },
            {
            'id'          : 2,
            'img_src'     : 'test@test.com2',
            'description' : 'test_description2',
                }
            ]        
        
        response = self.client.get(reverse('IndependentImage'))
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,data)
        
        
class ProductListRetrieveTestCase(APITestCase):
    def setUp(self):
        
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
        
        setup_product_image_list=[
            ProductImage(
                id          = 1, 
                product_id  = 1,
                img_src     = 'test_img1@test.com',
                page        = 'main',
                place       = 'list',
                description = 'test_desc1',
            ),
            ProductImage(
                id          = 2, 
                product_id  = 1,
                img_src     = 'test_img2@test.com',
                page        = 'detail',
                place       = 'list',
                description = 'test_desc2',
            ),
            ProductImage(
                id          = 3, 
                product_id  = 2,
                img_src     = 'test_img3@test.com',
                page        = 'main',
                place       = 'list',
                description = 'test_desc3',
            ),
            ProductImage(
                id          = 4, 
                product_id  = 2,
                img_src     = 'test_img4@test.com',
                page        = 'main',
                place       = 'list',
                description = 'test_desc4',
            ),
            ProductImage(
                id          = 5, 
                product_id  = 3,
                img_src     = 'test_img5@test.com',
                page        = 'main',
                place       = 'list',
                description = 'test_desc5',
            ),
        ]
        
        Product.objects.bulk_create(setup_product_list)
        ProductImage.objects.bulk_create(setup_product_image_list)
        
    def test_list_product_category_bread(self):
        
        data = [
            {
            "id"                   : 1,
            "category"             : 'bread',
            "product_name"         : 'test_product1',
            "price"                : 10000,
            "optional_description" : 'test_optional_description1',
            "description"          : 'test_description',
            "is_active"            : True,
            "product_images"       : [
                {
                'id'          : 1, 
                'product'     : 1,
                'img_src'     : 'test_img1@test.com',
                'page'        : 'main',
                'place'       : 'list',
                'description' : 'test_desc1',
            },
                {
                'id'          : 2, 
                'product'     : 1,
                'img_src'     : 'test_img2@test.com',
                'page'        : 'detail',
                'place'       : 'list',
                'description' : 'test_desc2',
            },
            ],
        },
        {
            "id"                   : 2,
            "category"             : 'bread',
            "product_name"         : 'test_product2',
            "price"                : 10000,
            "optional_description" : 'test_optional_description2',
            "description"          : 'test_description',
            "is_active"            : True,
            "product_images"       : [
                {
                'id'         : 3,
                'img_src'    : 'test_img3@test.com',
                'page'       : 'main',
                'place'      : 'list',
                'description': 'test_desc3',
                'product'    : 2
                },
                {
                'id'         : 4,
                'img_src'    : 'test_img4@test.com',
                'page'       : 'main',
                'place'      : 'list',
                'description': 'test_desc4',
                'product'    : 2
                }
                ],
        },
        ]
        
        #follow=True옵션을 주면 301에러를 피할 수 있음
        response = self.client.get('/products?category=bread',follow=True)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json(),data)
    
    def test_list_product_img_filter(self):
        
        data = [
            {
            "id"                   : 1,
            "category"             : 'bread',
            "product_name"         : 'test_product1',
            "price"                : 10000,
            "optional_description" : 'test_optional_description1',
            "description"          : 'test_description',
            "is_active"            : True,
            "product_images"       : [
                {
                'id'          : 1, 
                'product'     : 1,
                'img_src'     : 'test_img1@test.com',
                'page'        : 'main',
                'place'       : 'list',
                'description' : 'test_desc1',
            },
            ],
        },
        {
            "id"                   : 2,
            "category"             : 'bread',
            "product_name"         : 'test_product2',
            "price"                : 10000,
            "optional_description" : 'test_optional_description2',
            "description"          : 'test_description',
            "is_active"            : True,
            "product_images"       : [
                {
                'id'         : 3,
                'img_src'    : 'test_img3@test.com',
                'page'       : 'main',
                'place'      : 'list',
                'description': 'test_desc3',
                'product'    : 2
                },
                {
                'id'         : 4,
                'img_src'    : 'test_img4@test.com',
                'page'       : 'main',
                'place'      : 'list',
                'description': 'test_desc4',
                'product'    : 2
                }
                ],
        },
        {
            "id"                   : 3,
            "category"             : 'cake',
            "product_name"         : 'test_product3',
            "price"                : 10000,
            "optional_description" : 'test_optional_description3',
            "description"          : 'test_description',
            "is_active"            : True,
            "product_images"       : [
                {
                'id'         : 5,
                'img_src'    : 'test_img5@test.com',
                'page'       : 'main',
                'place'      : 'list',
                'description': 'test_desc5',
                'product'    : 3
                }
                ],
        },
        ]

        response = self.client.get('/products?img_filter=page:main,place:list',follow=True)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json(),data)
    
    def test_list_product_field_filtering(self):
        
        data = [
            {
            "id"                   : 1,
            "product_name"         : 'test_product1',
            "price"                : 10000,
            "description"          : 'test_description',
        },
        {
            "id"                   : 2,
            "product_name"         : 'test_product2',
            "price"                : 10000,
            "description"          : 'test_description',
        },
        {
            "id"                   : 3,
            "product_name"         : 'test_product3',
            "price"                : 10000,
            "description"          : 'test_description',
        },
        ]
        
        response = self.client.get('/products?fields=id,product_name,price,description',follow=True)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json(),data)
        
    def test_retrieve_product(self):
        data = {
            "id"                   : 1,
            "category"             : 'bread',
            "product_name"         : 'test_product1',
            "price"                : 10000,
            "optional_description" : 'test_optional_description1',
            "description"          : 'test_description',
            "is_active"            : True,
            "product_images"       : [
                {
                'id'          : 1, 
                'product'     : 1,
                'img_src'     : 'test_img1@test.com',
                'page'        : 'main',
                'place'       : 'list',
                'description' : 'test_desc1',
            },
                {
                'id'          : 2, 
                'product'     : 1,
                'img_src'     : 'test_img2@test.com',
                'page'        : 'detail',
                'place'       : 'list',
                'description' : 'test_desc2',
            },
            ],
        }
    
        response = self.client.get(reverse('ProductDetail',kwargs={'product_id':1}))
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,data)
        