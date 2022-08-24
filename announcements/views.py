from drf_spectacular.utils     import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
from rest_framework.response    import Response
from django.db.models           import Prefetch
from rest_framework             import generics
from rest_framework.views       import APIView
from rest_framework.permissions import IsAuthenticated
from core.permissions           import IsAdminOrReadOnly,IsAdminOrIsWriterOrForbidden
from announcements.models       import FAQ, QnA, QnAComment
from announcements.serializers  import FAQSerializer, QnASerializer, QnACommentSerializer
from core.cores                 import S3Uploader, query_debugger

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
    queryset           = QnA.objects.all().\
        select_related('user').\
            prefetch_related(Prefetch('qna_comments',queryset=QnAComment.objects.all().select_related('user')))
            
    serializer_class   = QnASerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)
    
    @query_debugger
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

@extend_schema(methods=['PUT'], exclude=True)
class QnADetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrIsWriterOrForbidden]
    queryset           = QnA.objects.all()
    serializer_class   = QnASerializer
    lookup_url_kwarg   = 'qna_id'
    lookup_field       = 'id'
    
    
@extend_schema(methods=['GET','PUT','PATCH','DELETE'], exclude=True)
class QnACommentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = QnACommentSerializer
    queryset           = QnAComment.objects.all()
    
    def perform_create(self, serializer):
        qna_id = self.kwargs.get('qna_id')
        user = self.request.user
        serializer.save(user = self.request.user,qna_id = qna_id)
    

@extend_schema(methods=['GET','PUT','PATCH'], exclude=True)
class QnACommenDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminOrIsWriterOrForbidden]
    serializer_class   = QnACommentSerializer
    queryset           = QnAComment.objects.all()
    lookup_url_kwarg   = 'comment_id'
    lookup_field       = 'id'
    
class NoticeAPIView(APIView):
    def post(self, request):
        print(request.data)
        # img1 = request.data.pop('img1')

        
        if request.FILES:
            s3_uploader = S3Uploader()
            print(request.FILES)
            for img in request.FILES:
                
                #getlist의 경우 여러장의 이미지를 하나의 키값으로 받을때 배열로 받는 메서드이고,
                #getitem의 경우 한장의 이미지가 하나의 키값에 존재할 때 사용할 수 있는 메서드이다.
                
                request.data.pop(img)
                
                img_data = request.FILES.__getitem__(img)
                s3_uploader.upload(img_data,f"backend/{img}")
                print(img)
                print(type(img))
                


        else:
            print("no bb")
        
        # print("----------")
        # print(img1)
        # print(type(img1))
        # print("----------")
        # s3_uploader = S3Uploader()
        # s3_uploader.upload(img1[0],"backend/testing_class3")
        
        
        
        # img2 = request.data.pop('img2')
        # img3 = request.data.pop('img3')
        print(request.data)
        return Response(request.data,status=200)