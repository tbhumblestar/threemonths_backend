from rest_framework.serializers import ModelSerializer
from announcements.models       import FAQ, QnA, QnAComment


class FAQSerializer(ModelSerializer):
    
    class Meta:
        model  = FAQ
        fields = ['id','question','answer','created_at']
        
        
class QnACommentSerializer(ModelSerializer):
    
    class Meta:
        model  = QnAComment
        fields = ['id','content','created_at']
        
        
class QnASerializer(ModelSerializer):
    qna_comments = QnACommentSerializer(many=True,read_only=True)
    
    class Meta:
        model  = QnA
        fields = ['id','title','content','qna_comments','created_at']