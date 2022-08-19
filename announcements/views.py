from drf_spectacular.utils     import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes

from rest_framework             import generics
from rest_framework.permissions import IsAuthenticated
from core.permissions          import IsAdminOrReadOnly,IsAdminOrIsWriterOrForbidden
from announcements.models      import FAQ, QnA, QnAComment
from announcements.serializers import FAQSerializer, QnASerializer, QnACommentSerializer


class FAQView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset         = FAQ.objects.all()
    serializer_class = FAQSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset         = QnA.objects.all()
    serializer_class = QnASerializer
    lookup_url_kwarg   = 'faq_id'
    lookup_field       = 'id'
    
    
class QnAView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset           = QnA.objects.all()
    serializer_class   = QnASerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)
        
class QnADetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrIsWriterOrForbidden]
    queryset           = QnA.objects.all()
    serializer_class   = QnASerializer
    lookup_url_kwarg   = 'q_and_a_id'
    lookup_field       = 'id'
    
    

class QnACommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = QnACommentSerializer
    queryset           = QnAComment.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)


class QnACommenDetailView(generics.DestroyAPIView):
    permission_classes = [IsAdminOrIsWriterOrForbidden]
    serializer_class   = QnACommentSerializer
    queryset           = QnAComment.objects.all()
    lookup_url_kwarg   = 'comment_id'
    lookup_field       = 'id'


    