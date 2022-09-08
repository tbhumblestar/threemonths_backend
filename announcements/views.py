import uuid

from rest_framework             import serializers
from rest_framework.response    import Response
from django.db.models           import Prefetch
from rest_framework             import generics
from rest_framework             import status
from rest_framework.views       import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils      import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes, extend_schema_view, inline_serializer
from django.db                  import transaction

from core.permissions           import IsAdminOrReadOnly,IsAdminOrIsWriterOrForbidden
from announcements.models       import FAQ, QnA, QnAComment, Notice
from announcements.serializers  import FAQSerializer, NoticeSerializer, QnASerializer, QnACommentSerializer
from core.cores                 import S3Handler, query_debugger


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
    queryset         = FAQ.objects.all()
    serializer_class = FAQSerializer
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
    
    
    
@extend_schema_view(
    get = extend_schema(
    description='## 권한 ## \n\n 누구나(비회원도) 가능',
    parameters=[
        OpenApiParameter(
            name        = 'fields',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "응답으로 받을 Notice 필드를 입력",
            examples    = [OpenApiExample(
                name           = 'fields',
                value          = 'id,title,created_at,img1_url,img1_s3_path...',
                parameter_only = OpenApiParameter.QUERY,
                description    = "필요한 필드의 이름을 ,로 구분해서 넣어주면 됩니다. \n\n 아무것도 넣어주지 않을 경우, 응답으로 상품의 모든 필드에 대한 정보를 얻을 수 있습니다."
                )]
            ),
    ],
    
),
    post=extend_schema(
        description='## 권한 ## \n\n 관리자만 가능',
        request=inline_serializer('notice_create',{
        "title"          : serializers.CharField(),
        "content"        : serializers.CharField(),
        "img1_url"       : serializers.FileField(),
        "img1_s3_path"   : serializers.FileField(),
        "img2_url"       : serializers.FileField(),
        "img2_s3_path"   : serializers.FileField(),
        "img3_url"       : serializers.FileField(),
        "img4_s3_path"   : serializers.FileField(),
        }
        )
    )
)   
class NoticeView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class   = NoticeSerializer
    queryset           = Notice.objects.all()
    
    def get_serializer_context(self):
        additional_context = {}

        #dyanamic field filtering
        want_fields     = self.request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))
        
        #context_update
        context = super().get_serializer_context()
        context.update(additional_context)
        
        return context

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        
        img_dict = {}
        
        if request.FILES:
            s3_handler = S3Handler()
            for img in request.FILES:
                
                request.data.pop(img)
                
                img_file = request.FILES.__getitem__(img)
                res_dict = s3_handler.upload(
                    file       = img_file,
                    Key        = f"backend/Notice/{str(uuid.uuid4())}",
                    field_name = f"{img}",
                )
                img_dict.update(res_dict)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,img_dict)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer,img_dict):
        user = self.request.user
        serializer.save(user=user,**img_dict)


@extend_schema(methods=['PUT'], exclude=True)
@extend_schema_view(
    get = extend_schema(
        description = "## 권한 ## \n\n 누구나(비회원도) 가능"),
    delete = extend_schema(
        description = "## 권한 ## \n\n 관리자만 가능"),
    patch = extend_schema(
        description = "## 권한 ## \n\n 관리자만 가능",
        parameters=[
        OpenApiParameter(
            name        = 'img_delete',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "해당 Notice의 이미지를 삭제할때 사용. [img1]라는 값을 보내줄 경우 해당 리뷰의 img1이 삭제되는 방식. []라는 값을 보낼 경우 아무기능도 하지 않음 ",
            examples    = [OpenApiExample(
                name           = 'img_delete',
                value          = 'ex) [img] , [], [img1,img2]',
                parameter_only = OpenApiParameter.QUERY,
                description    = "[img1] 또는 []만 허용. 그 외에는 에러 발생"
                )]
            )],
        request=inline_serializer('user',{
        "title"          : serializers.CharField(),
        "content"        : serializers.CharField(),
        "img1_url"       : serializers.FileField(),
        "img1_s3_path"   : serializers.FileField(),
        "img2_url"       : serializers.FileField(),
        "img2_s3_path"   : serializers.FileField(),
        "img3_url"       : serializers.FileField(),
        "img4_s3_path"   : serializers.FileField(),
            }
        )
    )
) 
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class   = NoticeSerializer
    queryset           = Notice.objects.all()
    lookup_url_kwarg   = 'notice_id'
    lookup_field       = 'id'
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        s3_handler = S3Handler()
        img_dict = {}
        if request.FILES:
            
            for img in request.FILES:

                img_s3_path = getattr(instance,f'{img}_s3_path')
                img_url     = getattr(instance,f'{img}_url')
                
                if img_s3_path:
                    s3_handler.delete(img_s3_path)
                    setattr(instance,f'{img}_s3_path',None)
                
                if img_url:
                    setattr(instance,f'{img}_url',None)
                
                img_file = request.FILES.__getitem__(img)
                res_dict = s3_handler.upload(
                    file       = img_file,
                    Key        = f"backend/Notice/{str(uuid.uuid4())}",
                    field_name = f"{img}",
                )
                img_dict.update(res_dict)
        
        if request.query_params.get('img_delete'):
            img_delete_list = request.query_params.get('img_delete').lstrip('[').rstrip(']').split(',')
        
            if img_delete_list[0]:
                for img in img_delete_list:
                    img_s3_path = getattr(instance,f'{img}_s3_path')
                    img_url     = getattr(instance,f'{img}_url')
                    
                    if img_s3_path != None:
                        s3_handler.delete(img_s3_path)

                    setattr(instance,f'{img}_s3_path',None)
                    setattr(instance,f'{img}_url',None)
                    
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer,img_dict)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def perform_update(self, serializer,img_dict):
        serializer.save(**img_dict)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance   = self.get_object()
        s3_handler = S3Handler()
        
        if instance.img1_s3_path:
            s3_handler.delete(instance.img1_s3_path)
        if instance.img2_s3_path:
            s3_handler.delete(instance.img2_s3_path)
        if instance.img3_s3_path:
            s3_handler.delete(instance.img3_s3_path)
        
        self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)