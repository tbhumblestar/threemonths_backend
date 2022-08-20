from rest_framework import serializers
from announcements.models       import FAQ, QnA, QnAComment


class FAQSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = FAQ
        fields = ['id','question','answer','created_at']
        
        
class QnACommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = QnAComment
        fields = ['id','content','created_at']
        
        
class QnASerializer(serializers.ModelSerializer):
    qna_comments = QnACommentSerializer(many=True,read_only=True)
    user_nickname = serializers.SerializerMethodField()
    
    class Meta:
        model  = QnA
        fields = ['id','title','content','qna_comments','created_at','user_nickname']
        
    def get_user_nickname(self,object):
        return object.user.nickname