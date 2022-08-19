from rest_framework.serializers import Serializer,ModelSerializer
from announcements.models       import FAQ, QnA, QnAComment


class FAQSerializer(ModelSerializer):
    
    class Meta:
        model  = FAQ
        fields = ['question','awnser']
        
class QnASerializer(ModelSerializer):
    
    class Meta:
        model  = QnA
        fields = ['title','content']
        
class QnACommentSerializer(ModelSerializer):
    
    class Meta:
        model  = QnAComment
        fields = ['content']