from rest_framework.serializers import Serializer,ModelSerializer
from announcements.models       import FAQ, QAndA, QAndAComment





class FAQSerializer(ModelSerializer):
    
    class Meta:
        model  = FAQ
        fields = ['question','awnser']