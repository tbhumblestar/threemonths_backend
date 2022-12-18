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
                                            OpenApiTypes,
                                            OpenApiResponse
)
from core.cores import send_sms,checking_email_unique
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
        "is_staff"    : serializers.CharField(),
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

            #카카오 서버측 에러
            if response.status_code != 200 :
                return Response({"message":response.json().get('msg')},status = status.HTTP_400_BAD_REQUEST)
            response          = response.json()
            
            #카카오 서버로부터 이메일을 받지 못한 경우
            email             = response.get('kakao_account').get('email')
            if not email:
                return Response({"message":"Don't have Email information"},status=status.HTTP_400_BAD_REQUEST)
            
            #이메일이 이미 존재하는지를 확인. 존재할 경우 login_type을 반환. 존재하지 않을 경우 None
            email_login_type = checking_email_unique(email)
            if email_login_type:
                return Response({"message":"Email already exists","login_type":email_login_type},status=status.HTTP_409_CONFLICT)
            
            #카카오 서버로부터 전화번호를 받지 못한 경우
            contact_num       = response.get('kakao_account').get('phone_number')
            if not email:
                return Response({"message":"Don't have contact_num information"},status=status.HTTP_400_BAD_REQUEST)

            #
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
            name          = "요청",
            description   = "전화번호, 이메일이 고유해야 하며, 아이디와 비밀번호도 양식에 맞아야 함",
            request_only = True,
            value = {
                "nickname"    : "tester",
                "email"       : "test@gmail.com",
                "contact_num" : '010-0000-0000',
                "password"    : "!test123!",
                "login_type"  : "SiteLogin"
    },
        ),
        
    ],
    request=inline_serializer('sitesignup',{
        "nickname"     : serializers.CharField(),
        "email"        : serializers.CharField(),
        "contact_num"  : serializers.CharField(),
        "password"     : serializers.CharField(),
        "login_type"   : serializers.CharField(),
        },
        ),
    responses={
        201: OpenApiResponse(description='사이트 회원가입 성공'),
        400: OpenApiResponse(description='Body 데이터 키 에러 / 이메일 양식 틀림 / 비밀번호 양식 틀림'),
        409: OpenApiResponse(description='이메일 또는 전화번호 중복'),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            create_data = {
                'nickname'     : request.data['nickname'],
                'email'        : request.data['email'],
                'contact_num'  : request.data['contact_num'],
                'password'     : request.data['password'],
                'login_type'   : request.data['login_type'],
            }
            
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        #이메일이 이미 존재하는지를 확인. 존재할 경우 login_type을 반환. 존재하지 않을 경우 None
        email_login_type = checking_email_unique(request.data['email'])
        if email_login_type:
            return Response({"message":"Email already exists","login_type":email_login_type},status=status.HTTP_409_CONFLICT)
        
        if create_data['email'].count('@')>=2:
            return Response({'message':'Wrong_type_Email'},status=status.HTTP_400_BAD_REQUEST)
        
        #전화번호
        if User.objects.filter(contact_num=create_data['contact_num']):
            return Response({'message':'Contact_num already exists'},status=status.HTTP_409_CONFLICT)
        
        #회원가입
        user = User.objects.create_user(**create_data)
        return Response(status=status.HTTP_201_CREATED)


class SiteLoginView(APIView):
    queryset = None
    serializer_class = None
    
    @extend_schema(
    description='서비스 자체 로그인',
    examples=[
        OpenApiExample(
            name          = "요청",
            description   = "이메일과 비밀번호를 받음",
            request_only = True,
            value = {
                "email"       : "test@gmail.com",
                "password"    : "!test123!",
                "login_type"  : "SiteLogin"
    },
        ),
        OpenApiExample(
            name          = "응답(201)",
            description   = '사이트 로그인 성공, jwt토큰반환',
            response_only = True,
            status_codes  = [201],
            value = {
                "jwt"      : {
                    "refresh": "eyJ0eX......lCCSW1g",
                    "access": "eyJ0eX......g77rSqw"
    }
},
        )
    ],
    request=inline_serializer('sitesignup',{
        "email"        : serializers.CharField(),
        "password"     : serializers.CharField(),
        "login_type"   : serializers.CharField(),
        },
        ),
    responses={
        201 : inline_serializer(
            'jwt',
            fields = {
                'refresh' : serializers.CharField(),
                'access'  : serializers.CharField(),
                }),
        400: OpenApiResponse(description='Body 데이터 키 에러'),
        401: OpenApiResponse(description='받은 정보와 일치하는 유저가 없음'),
        500: OpenApiResponse(description='서버 측 에러')
        }
    )
    def post(self,request,*args,**kwargs):
        
        try:
            email = request.data['email']
            password = request.data['password']
            login_type = request.data['login_type']
            
        
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            
            #로그인 타입이 다를 경우
            if user.login_type != login_type:
                return Response({"message":f"This email is registered as {user.login_type}."},status=status.HTTP_401_UNAUTHORIZED)
            
            #비밀번호가 틀릴 경우
            if not user.check_password(password):
                return Response({"message":"There are no users matching the information"},status=status.HTTP_401_UNAUTHORIZED)
            
            #JWT
            refresh = RefreshToken.for_user(user)
            jwt_token = {
            'refresh' : str(refresh),
            'access'  : str(refresh.access_token),
        }
            return Response(jwt_token,status=status.HTTP_201_CREATED)
        
        #이메일이 일치하는 경우가 없을 경우
        return Response({"message":"There are no users matching the information"},status=status.HTTP_401_UNAUTHORIZED)
            

class RunSMSAuthView(APIView):
    """
    폰번호를 받고, 해당 번호로 5자리의 문자인증을 실행
    """
    @extend_schema(
    description='번호를 받고, 받은 번호로 문자인증을 수행',
    examples=[
        OpenApiExample(
            name          = "요청",
            description   = "받은 번호에 랜덤한 5자리 문자인증을 수행<br/><br/>반드시 000-0000-0000 형태로 전화번호를 받아야 함",
            request_only = True,
            value = {
                "contact_num" : '010-0000-0000',
    },
        )
    ],
    request=inline_serializer('RunSMSAuth',{
        "contact_num"  : serializers.CharField(),
        },
        ),
    responses={
        201: OpenApiResponse(description='문자인증번호 송신 성공'),
        400: OpenApiResponse(description='Body 데이터 키 에러'),
        500: OpenApiResponse(description='네이버 서버오류 / 예상치 못한 서버 오류'),
        }
    )
    def post(self,request,*args,**kwargs):
        
        try:
            contact_num = request.data['contact_num']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        ### fix
        # 추가할 것 : 테스트코드(mock)
        
        sms_check_num =  str(random.randint(10000,99999))
        message       =  f'Threemonths 홈페이지 인증번호는 [{sms_check_num}] 입니다'
        res           =  send_sms(phone_number=contact_num,message=message)
        
        #NaverCloud는 202일때만 성공
        if res.get('statusCode') != "202":
            return Response({'message':'NAVER_CLOUD_ERROR'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #기존에 있던 인증코드삭제
        if SMSAuth.objects.filter(contact_num=contact_num):
            SMSAuth.objects.filter(contact_num=contact_num).delete()
            
        SMSAuth.objects.create(contact_num=contact_num,sms_check_num=sms_check_num)

        return Response(status=status.HTTP_201_CREATED)


class CheckSMSAuthView(APIView):
    @extend_schema(
    description='폰번호와 문자인증번호를 받아, 문자인증을 성공여부를 판별',
    examples=[
        OpenApiExample(
            name          = "요청",
            description   = "번호(contact_num)는 문자형, 문자인증번호(sms_check_num)는 숫자형 <br/><br/> 문자인증에 성공한 문자인증번호는 바로 삭제됨(즉 동일한 인증번호를 다시 보낼 경우 실패함)",
            request_only = True,
            value = {
                "contact_num" : '010-0000-0000',
                "sms_check_num" : 36338,
    },
        )
    ],
    request=inline_serializer('CheckSMSAuth',{
        "contact_num"  : serializers.CharField(),
        "sms_check_num"  : serializers.IntegerField(),
        },
        ),
    responses={
        200: OpenApiResponse(description='문자인증 성공'),
        204: OpenApiResponse(description='문자인증 실패(휴대폰번호와 인증번호가 일치하지 않음)'),
        400: OpenApiResponse(description='Body 데이터 키 에러'),
        500: OpenApiResponse(description='예상치 못한 서버 오류'),
        }
    )
    def post(self,request,*args,**kwargs):
        try:
            contact_num = request.data['contact_num']
            sms_check_num = request.data['sms_check_num']
            
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        #성공
        if SMSAuth.objects.filter(contact_num=contact_num,sms_check_num=sms_check_num):
            SMSAuth.objects.filter(contact_num=contact_num,sms_check_num=sms_check_num).delete()
            return Response(status=status.HTTP_200_OK)
        
        #실패
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class GetEmailByContactNumView(APIView):
    @extend_schema(
    description='아이디 찾기에서 사용<br/><br/>문자인증에 성공하고나서 사용<br/><br/> 번호를 받아서 해당 번호로 검색되는 email이 있는지 확인',
    examples=[
        OpenApiExample(
            name          = "요청",
            description   = "번호(contact_num)는 문자형",
            request_only = True,
            value = {
                "contact_num" : '010-0000-0000',
    },
        ),
        OpenApiExample(
            name          = "응답 : 성공(200)",
            description   = "받은 번호로 등록된 이메일을 반환<br/><br/>앞의 두글자 이하로는 *로 표시",
            response_only =  True,
            value = {
                "email" : 'te**@naver.com',
    },
        )
    ],
    request=inline_serializer('GetEmailByContactNum',{
        "contact_num"  : serializers.CharField(),
        },
        ),
    responses={
        200: inline_serializer('GetEmailByContactNum',{
        "email"  : serializers.CharField(),
        },
        ),
        204: OpenApiResponse(description='해당 번호로 등록된 이메일이 없음'),
        400: OpenApiResponse(description='Body 데이터 키 에러'),
        500: OpenApiResponse(description='예상치 못한 서버 오류'),
        }
    )
    def post(self,request):
        try:
            contact_num = request.data['contact_num']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        #fix : contact_num 여러 개 일 수도 잇음.. 이 부분 모델에서 체크해야 함
        if User.objects.filter(contact_num=contact_num):
            user = User.objects.get(contact_num=contact_num)
            
            email_split = user.email.split("@")
            email_first = email_split[0] if len(email_split[0])<= 2 else email_split[0][:2] + "*" * (len(email_split[0])-2)
            email_last = email_split[1]
            email = email_first + "@" + email_last
            
            return Response({'email':email},status=status.HTTP_200_OK)
        return Response({'message':'NO_USER'},status=status.HTTP_204_NO_CONTENT)


class MatchEmailAndContactNumView(APIView):
    @extend_schema(
    description='비밀번호 찾기에서 사용<br/><br/>이메일과 번호를 받고, 해당 이메일과 번호를 가진 유저가 있는지 확인',
    examples=[
        OpenApiExample(
            name          = "요청",
            description   = "번호(contact_num)는 문자형",
            request_only = True,
            value = {
                "contact_num" : '010-0000-0000',
                "email":"test@test.com"
    },
        ),
        OpenApiExample(
            name          = "요청성공(200)",
            description   = "받은 번호와 이메일을 가진 유저의 id를 반환",
            response_only =  True,
            value = {
                "user_id" : 75,
    },
        )
    ],
    request=inline_serializer('CheckEmailAndContactNum',{
        "user_id"  : serializers.CharField(),
        },
        ),
    responses={
        200: inline_serializer('CheckEmailAndContactNum',{
        "email"  : serializers.IntegerField(),
        },
        ),
        204: OpenApiResponse(description='해당 번호와 이메일을 가진 유저가 없음'),
        400: OpenApiResponse(description='Body 데이터 키 에러'),
        500: OpenApiResponse(description='예상치 못한 서버 오류'),
        }
    )
    def post(self,request):
        try:
            contact_num = request.data['contact_num']
            email        = request.data['email']
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email = email,contact_num=contact_num):
            user = User.objects.get(email=email,contact_num=contact_num)
            return Response({"user_id" : user.id},status=status.HTTP_200_OK)
        
        return Response({'message':'NO_USER'},status=status.HTTP_204_NO_CONTENT)
        


class SetNewPWView(APIView):
    """
    유저pk와 새 비밀번호를 받음
    비밀번호를 해시함수에 적용하여 저장
    """
    @extend_schema(
    description='유저pk와 새 비밀번호를 받음<br/><br/>비밀번호를 해시함수에 적용하여 저장',
    examples=[
        OpenApiExample(
            name          = "요청",
            description   = "번호(contact_num)는 문자형",
            request_only = True,
            value = {
                "user_id" : 75,
                "new_pw":"!abcd2345A!"
    },
        ),
    ],
    request=inline_serializer('SetNewPW',{
        "user_id"  : serializers.CharField(),
        "new_pw"  : serializers.CharField(),
        },
        ),
    responses={
        200: OpenApiResponse(description='비밀번호 변경 성공'),
        400: OpenApiResponse(description='Body 데이터 키 에러 / 해당 id를 가진 유저가 존재하지 않음'),
        500: OpenApiResponse(description='예상치 못한 서버 오류'),
        }
    )
    def post(self,request):
        try:
            user_id = request.data['user_id']
            new_pw  = request.data['new_pw']
            
            user = User.objects.get(id=user_id)
            user.set_password(new_pw)
            user.save()
        except KeyError:
            return Response({'message':'KEY_ERROR'},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message':'NO_USER'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK)
