from drf_spectacular.utils     import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes

from rest_framework             import generics
from rest_framework.permissions import IsAuthenticated
from core.permissions          import IsAdminOrReadOnly,IsAdminOrIsWriterOrForbidden
from announcements.models      import FAQ, QnA, QnAComment
from announcements.serializers import FAQSerializer, QnASerializer, QnACommentSerializer

@extend_schema(methods=['Post','PUT','patch','Delete'], exclude=True)
class FAQView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset         = FAQ.objects.all()
    serializer_class = FAQSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)


@extend_schema(methods=['Post','PUT','patch','Delete'], exclude=True)
class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset         = QnA.objects.all()
    serializer_class = QnASerializer
    lookup_url_kwarg   = 'faq_id'
    lookup_field       = 'id'
    
@extend_schema(methods=['POST'], exclude=True)
class QnAView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset           = QnA.objects.all().prefetch_related('qna_comments')
    serializer_class   = QnASerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)

@extend_schema(methods=['PUT'], exclude=True)
class QnADetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrIsWriterOrForbidden]
    queryset           = QnA.objects.all()
    serializer_class   = QnASerializer
    lookup_url_kwarg   = 'qna_id'
    lookup_field       = 'id'
    
    
@extend_schema(methods=['GET','PUT','patch','Delete'], exclude=True)
class QnACommentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = QnACommentSerializer
    queryset           = QnAComment.objects.all()
    
    def perform_create(self, serializer):
        qna_id = self.kwargs.get('qna_id')
        user = self.request.user
        serializer.save(user = self.request.user,qna_id = qna_id)


@extend_schema(methods=['GET','PUT','patch'], exclude=True)
class QnACommenDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminOrIsWriterOrForbidden]
    serializer_class   = QnACommentSerializer
    queryset           = QnAComment.objects.all()
    lookup_url_kwarg   = 'comment_id'
    lookup_field       = 'id'