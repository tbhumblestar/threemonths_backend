from rest_framework.serializers import Serializer,ModelSerializer
from announcements.models       import FAQ, QnA, QnAComment


class FAQSerializer(ModelSerializer):
    
    class Meta:
        model  = FAQ
        fields = ['id','question','awnser']
        
        
class QnACommentSerializer(ModelSerializer):
    
    class Meta:
        model  = QnAComment
        fields = ['id','content']
        
        
class QnASerializer(ModelSerializer):
    qna_comments = QnACommentSerializer(many=True,read_only=True)
    
    class Meta:
        model  = QnA
        fields = ['id','title','content','qna_comments']