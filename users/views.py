from rest_framework                  import serializers
from rest_framework                  import status
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response         import Response
from rest_framework.views            import APIView
from django.contrib.auth             import get_user_model
from django.core.exceptions          import ObjectDoesNotExist
from drf_spectacular.utils           import (extend_schema,
                                            OpenApiParameter,
                                            OpenApiExample,
                                            inline_serializer,
                                            OpenApiTypes
)
from core.cores import send_sms
from users.models import SMSAuth


from datetime   import datetime,timedelta
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
                "nickname" : "tester",
                "email"    : "test@gmail.com",
                "id"       : 1,
                "jwt"      : {
                    "refresh": "eyJ0eX......lCCSW1g",
                    "access": "eyJ0eX......g77rSqw"
    }
},
        )
    ],
    responses={200    : inline_serializer('user',{
        "nickname"    : serializers.CharField(),
        "email"       : serializers.EmailField(),
        "id"          : serializers.IntegerField(),
        "contact_num" : serializers.CharField(),
        "jwt"         : inline_serializer(
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
            
            email             = response.get('kakao_account').get('email')
            if not email:
                return Response({"message":"Don't have Email information"},status=status.HTTP_400_BAD_REQUEST)
            
            contact_num       = response.get('kakao_account').get('phone_number')
            if not email:
                return Response({"message":"Don't have contact_num information"},status=status.HTTP_400_BAD_REQUEST)

            contact_num = '0' + contact_num[4:]
            
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
                    'contact_num'      : contact_num,
                }
            )
            
            data = {}
            data['nickname'] = user.nickname
            data['email']    = user.email
            data['id']       = user.id
            data['is_staff'] = user.is_staff
            
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


class SiteSignUpView(APIView):

    @extend_schema(
    description='서비스 자체 회원가입',
    examples=[
        OpenApiExample(
            name          = "POST body example",
            description   = "이메일과 전화번호가 중복되지 않을 경우 ",
            request_only  = True,
            status_codes  = [200],
            value = {
                "nickname"    : "tester",
                "email"       : "test@gmail.com",
                "contact_num" : 1,
                "password"    : 'abcd1234'
    }
        )
    ],
)
    def post(self, request, *args, **kwargs):
        try:
            
            create_data = {
                'nickname'     : request.data['nickname'],
                'email'        : request.data['email'],
                'contact_num'  : request.data['phone_number'],
                'password'     : request.data['password'],
                'login_type'   : 'SiteLogin'
            }
            
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        #이메일 존재하는지 검증
        if User.objects.filter(email=create_data['email']):
            return Response({'message':'ALREADY_EXIST_EMAIL'},status=status.HTTP_400_BAD_REQUEST)
        
        #전화번호
        if User.objects.filter(contact_num=create_data['contact_num']):
            return Response({'message':'ALREADY_EXIST_CONTACT_NUM'},status=status.HTTP_400_BAD_REQUEST)
        
        #회원가입
        user = User.objects.create_user(**create_data)

        return Response(status=status.HTTP_201_CREATED)
    

class RunSMSAuthView(APIView):
    """
    폰번호를 받고, 해당 번호로 5자리의 문자인증을 실행
    """
    def post(self,request,*args,**kwargs):
        
        try:
            phone_number = request.data['phone_number']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        ### fix
        # 추가할 것 : 테스트코드(mock)
        
        sms_check_num =  str(random.randint(10000,99999))
        message       =  f'Threemonths 홈페이지 인증번호는 [{sms_check_num}] 입니다'
        res           =  send_sms(phone_number=phone_number,message=message)
        
        #NaverCloud는 202일때만 성공
        if res.get('statusCode') != "202":
            return Response({'message':'NAVER_CLOUD_ERROR'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #기존에 있던 인증코드삭제
        if SMSAuth.objects.filter(contact_num=phone_number):
            SMSAuth.objects.filter(contact_num=phone_number).delete()
            
        SMSAuth.objects.create(contact_num=phone_number,sms_check_num=sms_check_num)

        return Response(sms_check_num,status=status.HTTP_201_CREATED)



            
        

class GetEmailByContactNumView(APIView):
    """
    아이디 찾기 과정에서 사용되는 View
    문자인증에 성공했을 경우, 번호를 받아서 해당 번호로 검색되는 email이 있는지 확인
    #fix : phone_number가 여러 개 일 수도 잇음.. 이 부분 모델에서 체크해야 함
    """
    def post(self,request):
        try:
            contact_num = request.data['phone_number']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        #fix : contact_num 여러 개 일 수도 잇음.. 이 부분 모델에서 체크해야 함
        if User.objects.filter(contact_num=contact_num):
            user = User.objects.get(contact_num=contact_num)
            return Response({'email':user.email},status=status.HTTP_200_OK)
        
        return Response({'message':'NO_USER'},status=status.HTTP_400_BAD_REQUEST)


class CheckEmailAndContactNumView(APIView):
    """
    Email과 번호를 받고, 이에 일치하는 유저가 있는지 확인
    """
    def post(self,request):
        try:
            contact_num = request.data['phone_number']
            email        = request.data['email']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email = email,contact_num=contact_num):
            user = User.objects.get(email=email,contact_num=contact_num)
            return Response({user.id},status=status.HTTP_200_OK)
        
        return Response({'message':'NO_USER'},status=status.HTTP_400_BAD_REQUEST)
        


class SetNewPWView(APIView):
    """
    유저pk와 새 비밀번호를 받음
    비밀번호를 해시함수에 적용하여 저장
    """
    def post(self,request):
        try:
            user_id = request.data['user_id']
            new_pw  = request.data['new_pw']
            
            user = User.objects.get(id=user_id)
            print(new_pw)
            user.set_password(new_pw)
            user.save()
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message':'NO_USER'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK)
