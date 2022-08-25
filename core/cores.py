import functools, time, datetime
from django.db   import connection, reset_queries
from django.conf import settings
import boto3
import secret_settings

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
        
    def upload(self,file,Key,field_name='img',content_type='image/jpeg'):

        
        #https://stackoverflow.com/questions/72208629/share-jpeg-file-stored-on-s3-via-url-instead-of-downloading
        # 'content-type' : 'multipart/form-data'
        self.client.upload_fileobj(file,secret_settings.AWS_STORAGE_BUCKET_NAME,Key,ExtraArgs={'ContentType':content_type})
        
        res_dict = {
            f'{field_name}_s3_path' : Key,
            f'{field_name}_url'     : f'https://s3.{secret_settings.S3_REGION}.amazonaws.com/{secret_settings.AWS_STORAGE_BUCKET_NAME}/{Key}'
        }
        
        return res_dict
    
    def delete(self,Key):
        self.client.delete_object(Bucket=secret_settings.AWS_STORAGE_BUCKET_NAME,Key=Key)

    
