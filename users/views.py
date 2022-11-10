from rest_framework                  import serializers
from rest_framework                  import status
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response         import Response
from rest_framework.views            import APIView
from django.contrib.auth             import get_user_model
from drf_spectacular.utils           import (extend_schema,
                                            OpenApiParameter,
                                            OpenApiExample,
                                            inline_serializer,
                                            OpenApiTypes
)
from core.cores import send_sms
from .models    import SMSAuth
import requests, random

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
            
            return Response(data,status=status.HTTP_201_CREATED)
        
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
        

class RunSMSAuth(APIView):
    """
    폰번호를 받고, 해당 번호로 5자리의 문자인증을 실행
    """
    def post(self,request,*args,**kwargs):
        
        try:
            phone_number = request.data['phone_number']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        
        ### fix
        # 추가할 것 : 문자인증 안됐을 때 DB에 저장되지 않게 할 것
        # 추가할 것 : 해당 번호로 인증이 있다면, 새로만들어서 저장
        # 추가할 것 : 테스트코드(mock)
        
        sms_check_num = str(random.randint(10000,99999))
        message       = f'Threemonths 홈페이지 인증번호는 [{sms_check_num}] 입니다'
        res           = send_sms(phone_number=phone_number,message=message)
        
        #202일때만 성공
        if res.get('statusCode') != "202":
            return Response({'message':'NAVER_CLOUD_ERROR'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #혹시 기존에 동일한 번호로 인증데이터가 남아있다면 전부 삭제하고, 새로 객체를 만들어 저장
        #번호 인덱스 추가해야 함
        SMSAuth.objects.filter(phone_number = phone_number).delete()
        SMSAuth.objects.create(phone_number=phone_number,sms_check_num=sms_check_num)
        
        return Response(res,status=status.HTTP_201_CREATED)


class CheckSMSAuth(APIView):
    """
    폰번호, 문자인증 입력값을 받아 문자인증 일치여부 확인
    """
    def post(self,request):
        
        try:
            phone_number  = request.data['phone_number']
            sms_check_num = request.data['sms_check_num']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        if SMSAuth.objects.filter(phone_number=phone_number,sms_check_num=sms_check_num):
            SMSAuth.objects.get(phone_number=phone_number,sms_check_num=sms_check_num).delete()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_401_UNAUTHORIZED)

class CheckEmailAndContact(APIView):
    """
    Email과 번호를 받고, 이에 일치하는 유저가 있는지 확인
    """
    def post(self,request):
        pass
    
class SetnewPW(APIView):
    """
    유저pk와 새 비밀번호를 받음
    비밀번호를 해시함수에 적용하여(set_password)저장
    """
    def post(self,request):
        pass