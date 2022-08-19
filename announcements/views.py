from drf_spectacular.utils   import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes

from rest_framework import generics
from core.permissions import IsAdminOrReadOnly
from announcements.models import FAQ, QAndA, QAndAComment
from announcements.serializers import FAQSerializer


class FAQView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset         = FAQ.objects.all()
    serializer_class = FAQSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)
        
class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset         = FAQ.objects.all()
    serializer_class = FAQSerializer
    lookup_url_kwarg   = 'faq_id'
    lookup_field       = 'id'