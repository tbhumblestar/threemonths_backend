from rest_framework.test import APITestCase
from rest_framework      import status
from django.urls         import reverse

from products.models import IndependentImage

class IndependentImageListTestCase(APITestCase):
    def setUp(self):
        test_indenpendent_image_list = [
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
            test_indenpendent_image_list
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
        self.assertEqual(response.json(),data)