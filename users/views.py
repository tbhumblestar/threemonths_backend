from email import header
from attr import field
import requests

from rest_framework                  import serializers
from rest_framework                  import status
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response         import Response
from rest_framework.views            import APIView
from drf_spectacular.utils           import (extend_schema,
                                            OpenApiParameter,
                                            OpenApiExample,
                                            OpenApiResponse,
                                            inline_serializer,
                                            OpenApiTypes
)

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
    
    queryset = None
    serializer_class = None
    
    @extend_schema(
    description='Check Kakao access_token and return JWT_TOKEN',
    parameters=[
        OpenApiParameter(
            name        = 'kakao_access_token',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.HEADER,
            required    = True,
            description = "kaokao_access_token",
            examples    = [OpenApiExample(
                name        = "access_token",
                value       = 'Qyyq0_oFsinGpu1LWIfxU_mSiKpwOFxfHsMIvgZGCj10lwAAAYJ0_5Uv',
                description = "access_token을 바로 넣어주면 됩니다"
                )]
            ),
    ],
    examples=[
        OpenApiExample(
            name          = "success_example",
            description   = "access_token이 유효할 경우 획득할 수 있음",
            response_only = True,
            status_codes  = [200],
            value = {
                "nickname" : "김영빈",
                "email"    : "colock123@gmail.com",
                "id"       : 1,
                "jwt"      : {
                    "refresh": "eyJ0eX......lCCSW1g",
                    "access": "eyJ0eX......g77rSqw"
    }
},
        )
    ],
    responses={200 : inline_serializer('user',{
        "nickname" : serializers.CharField(),
        "email"    : serializers.EmailField(),
        "id"       : serializers.IntegerField(),
        "jwt"      : inline_serializer(
            'jwt',
            fields = {
                'refresh' : serializers.CharField(),
                'access'  : serializers.CharField(),
            }
            ),
    }
                                ),}
)
    def post(self,request,*args,**kwargs):
        
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