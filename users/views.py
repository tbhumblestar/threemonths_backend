import requests

from rest_framework                  import status
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response         import Response
from rest_framework.views            import APIView

from django.contrib.auth import get_user_model

User = get_user_model()

def request_kakao(token,func):
    kakao_url_dict = {
        'login'  : "https://kapi.kakao.com/v2/user/me",
        'logout' : "https://kapi.kakao.com/v1/user/logout"
    }
    
    kakao_url = kakao_url_dict[func]
    header ={
        "Content-Type"  : "application/x-www-form-urlencoded",
        "Authorization" : token,
    }
    
    return requests.get(kakao_url,headers=header)

class KaKaoLoginView(APIView):
    def post(self,request):
        
        try:
            token = f"Bearer {request.headers.get('Authorization')}"
            
            response          = request_kakao(token,'login')
            if response.status_code != 200 :
                return Response({"message":response.json().get('msg')},status = status.HTTP_400_BAD_REQUEST)
            response          = response.json()
            
            email             = response.get('kakao_account').get('email',None)
            if not email:
                return Response({"message":"Don't have Email information"},status=status.HTTP_400_BAD_REQUEST)
            
            kakao_id          = response.get('id')
            nickname          = response.get('properties').get('nickname')
            profile_image_url = response.get('kakao_account').get('profile').get('thumbnail_image_url')
            
            user,created = User.objects.get_or_create(
                kakao_id=kakao_id, #kakao_id를 기준으로 get_or_create결정
                defaults = {
                    "nickname"         : nickname,
                    "profile_image_url": profile_image_url,
                    "email"            : email,
                    "login_type"       : "KakaoLogin",
                }
            )
            
            data = {}
            data['nickname'] = user.nickname
            data['email']    = user.email
            data['id']       = user.id
            
            #JWT
            refresh = RefreshToken.for_user(user)
            data['jwt'] = {
            'refresh' : str(refresh),
            'access'  : str(refresh.access_token),
        }   
            
            if created:
                user.set_unusable_password()
                user.save() #save해주지 않으면 db에 저장되지 않음
                
                return Response(data,status=status.HTTP_201_CREATED)
            
            return Response(data,status=status.HTTP_200_OK)
        
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        
class KaKaoLogOutView(APIView):
    def post(self,request):
                
        try:
            token = f"Bearer {request.headers.get('Authorization')}"

            response = request_kakao(token,'logout')
            if response.status_code != 200 :
                return Response({"message":response.json().get('msg')},status = status.HTTP_400_BAD_REQUEST)
            
            return Response({"message":"success logout"},status=status.HTTP_200_OK)
        
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)