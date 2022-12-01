from django.db           import connection, reset_queries
from django.conf         import settings
from django.contrib.auth import get_user_model
from typing              import Union
import functools, time, datetime, boto3, requests, hashlib, hmac, base64
import secret_settings

from threemonths.settings            import (NAVER_SMS_SERVICE_ID,NAVER_ACCESS_KEY_ID,NAVER_SECRET_KEY,call_number)


User = get_user_model()


def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        #  - 1 if len(connection.queries) else 0
        print(f"-------------------------------------------------------------------")
        print(f"start_time :{datetime.datetime.now()}")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.3f}s")
        print(f"-------------------------------------------------------------------")
        return result
    return wrapper


class S3Handler():
    
    def __init__(self):
        self.client = boto3.client('s3',aws_access_key_id=secret_settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=secret_settings.AWS_SECRET_ACCESS_KEY)
        
    def upload(self,file,Key,field_name='img',content_type='image/jpeg') -> dict[str,str]:

        #https://stackoverflow.com/questions/72208629/share-jpeg-file-stored-on-s3-via-url-instead-of-downloading
        # 'content-type' : 'multipart/form-data'
        self.client.upload_fileobj(file,secret_settings.AWS_STORAGE_BUCKET_NAME,Key,ExtraArgs={'ContentType':content_type})
        
        res_dict = {
            f'{field_name}_s3_path' : Key,
            f'{field_name}_url'     : f'https://s3.{secret_settings.S3_REGION}.amazonaws.com/{secret_settings.AWS_STORAGE_BUCKET_NAME}/{Key}'
        }
        
        return res_dict
    
    def delete(self,Key) -> None:
        self.client.delete_object(Bucket=secret_settings.AWS_STORAGE_BUCKET_NAME,Key=Key)


def make_signature(access_key, secret_key, method, uri, timestmap):
    """
    네이버 클라우드api에서 사용할 시그니처를 생성
    """
    timestamp = str(int(time.time() * 1000))
    secret_key = bytes(secret_key, 'UTF-8')
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey


def send_sms(phone_number:str,message:str):
    """
    문자롤 보낼 번호와 보낼 메세지를 인자로 넣어주면 \n
    미리 등록된 발신번호로 문자가 발송됨
    """
    
    phone_number = phone_number.replace('-','')
    
    sms_uri              = f"/sms/v2/services/{NAVER_SMS_SERVICE_ID}/messages"
    sms_url              = f"https://sens.apigw.ntruss.com{sms_uri}"
    sms_access_key       = NAVER_ACCESS_KEY_ID
    sms_secret_key       = NAVER_SECRET_KEY
    sms_type             = "SMS"
    sms_from_countryCode = 82 
    sms_call_number      = call_number

    # uri
    uri = sms_uri
    #  URL
    url = sms_url
    # access key , secrek_key
    access_key = sms_access_key
    secret_key = sms_secret_key
    
    #헤더에 사용할 timestamp
    timestamp = str(int(time.time() * 1000))
    
    #헤더에 사용할 key
    #url이 아니라 uri를 넣어준다!
    key = make_signature(access_key, secret_key, 'POST', uri, timestamp)
    
    headers = {
    'Content-Type'            : 'application/json; charset=utf-8',
    'x-ncp-apigw-timestamp'   : timestamp,
    'x-ncp-iam-access-key'    : access_key,
    'x-ncp-apigw-signature-v2': key
    }
    
    body = {
            "type"        : sms_type,
            "contentType" : "COMM",
            "countryCode" : sms_from_countryCode,
            "from"        : call_number,
            "content"     : message,
            "messages"    :
                [{
                    "to"      : phone_number,
                    "content" : message,
                }]
            }
    
    res = requests.post(url, json=body, headers=headers)
    return res.json()


def checking_email_unique(email:str):
    """
    email(str)을 받아서 중복된 이메일이 있는지를 확인 \n
    있다면, 로그인타입(KaKao | SiteLogin)을 반환 \n
    없다면, None을 반환
    """
    if User.objects.filter(email=email):
        user = User.objects.get(email=email)
        return user.login_type
    
    return None