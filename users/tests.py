from rest_framework.test             import APITestCase
from rest_framework                  import status
from django.urls                     import reverse
from unittest.mock                   import patch, MagicMock
from django.contrib.auth             import get_user_model


from secret_settings import SECRET_KEY,algorithms

import jwt


User = get_user_model()

class LoginPostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            id                = 1,
            nickname          = 'test_nickname',
            email             = 'test_email@test.com',
            login_type        = "KakaoLogin",
            profile_image_url = 'test_profile_image_url@test.com',
            kakao_id          = 10
        )
        
        self.user.set_unusable_password()
        self.user.save()
        
        
    
    @patch('users.views.requests')
    def test_post_kakao_social_login(self,mocked_requests):
        
        ##테스트통신데이터
        class MockedResponse:
            @property
            def status_code(self):
                return 200
            
            def json(self):
                return {
                    "id": 10,
                    "properties": {
                        "nickname": "test_nickname",
                    },
                    "kakao_account": {
                        "profile": {
                            "profile_image_url": 'test_profile_image_url@test.com',
                        },
                        "email": 'test_email@test.com',
                    }
                }
                
        mocked_requests.get = MagicMock(return_value=MockedResponse())

        headers = {"HTTP_Authorization": "access_token"} #임시로 넣어주는 access_token. 어차피 상관X
        
        
        ##비교데이터
        data = {
            'id'       : 1,
            'nickname' : self.user.nickname,
            'email'    : self.user.email,
        }
        
        
        response = self.client.post(reverse('kakaologin'))
        

        
        jwt_access_token = response.data.pop('jwt').get('access')
        decoded_token = jwt.decode(jwt_access_token,SECRET_KEY,algorithms=algorithms)
        decoded_user_id = decoded_token.get('user_id')
        
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data,data)
        self.assertEqual(decoded_user_id,self.user.id)
        
    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()