from rest_framework       import serializers
from announcements.models import FAQ, QnA, QnAComment,Notice
from drf_spectacular.utils      import extend_schema_field



class FAQSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = FAQ
        fields = ['id','question','answer','created_at']
        
        
class QnACommentSerializer(serializers.ModelSerializer):
    
    user_nickname = serializers.SerializerMethodField()
    
    class Meta:
        model  = QnAComment
        fields = ['id','content','created_at','user_nickname']
        
    def get_user_nickname(self,object):
        return object.user.nickname
        
        
class QnASerializer(serializers.ModelSerializer):
    qna_comments = QnACommentSerializer(many=True,read_only=True)
    user_nickname = serializers.SerializerMethodField()
    
    class Meta:
        model  = QnA
        fields = ['id','title','content','qna_comments','created_at','user_nickname']
    
    def get_user_nickname(self,object):
        return object.user.nickname
    

class NoticeSerializer(serializers.ModelSerializer):
    
    img1_url     = serializers.CharField(read_only=True)
    img1_s3_path = serializers.CharField(read_only=True)
    img2_url     = serializers.CharField(read_only=True)
    img2_s3_path = serializers.CharField(read_only=True)
    img3_url     = serializers.CharField(read_only=True)
    img3_s3_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = Notice
        fields = ['id','title','created_at','content',
                    'img1_url','img1_s3_path','img2_url','img2_s3_path','img3_url','img3_s3_path'
                    ]
        
    #dynamic_filtering
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        want_fields = self.context.get('want_fields')
        
        
        if want_fields:
            allowed = set(want_fields)
            existing = set(self.fields)
            for field_name in existing-allowed:
                self.fields.pop(field_name)