import re, uuid

from django.db               import transaction
from rest_framework          import generics
from rest_framework          import status
from rest_framework.response import Response
from django_filters          import rest_framework as filters
from drf_spectacular.utils   import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes,inline_serializer,extend_schema_view
from rest_framework import serializers

from .models          import Product, IndependentImage, ProductImage
from .serializers     import IndependentImageSerializer, ProductSerializer
from core.filters     import IndependentImageFilter, ProductFilter
from core.cores       import S3Handler, query_debugger
from core.permissions import IsAdminOrReadOnly

class IndependentImageListView(generics.ListAPIView):
    queryset         = IndependentImage.objects.all()
    serializer_class = IndependentImageSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    filterset_class  = IndependentImageFilter

@extend_schema_view(
    post = extend_schema(
        description='## 설명 ## \n\n 상품 생성 \n\n 어드민 페이지에서 사용 \n\n <br/> \n\n ## 권한 ## \n\n 관리자만 가능',
        request=inline_serializer('product_create',{
            "product_name"         : serializers.CharField(),
            "category"             : serializers.CharField(),
            "price"                : serializers.IntegerField(),
            "description"          : serializers.CharField(),
            "optional_description" : serializers.CharField(),
            "is_active"            : serializers.BooleanField(),
            'main'                 : serializers.FileField(),
            'detail1'              : serializers.FileField(),
            'detail2'              : serializers.FileField(),
})
    ),
    get = extend_schema(
    description='## 설명 ## \n\n 상품 List 조회 \n\n <br/> \n\n ## 권한 ## \n\n 누구나(비회원도) 가능',
    parameters=[
        OpenApiParameter(
            name        = 'fields',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "응답으로 받을 상품의 필드를 입력",
            examples    = [OpenApiExample(
                name           = 'fields',
                value          = 'id,product_name,price,product_images,buying',
                parameter_only = OpenApiParameter.QUERY,
                description    = "필요한 필드의 이름을 ,로 구분해서 넣어주면 됩니다. \n\n 아무것도 넣어주지 않을 경우, 응답으로 상품의 모든 필드에 대한 정보를 얻을 수 있습니다."
                )]
            ),
        OpenApiParameter(
            name        = 'img_filter',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "사진을 선택하기 위한 필드",
            examples    = [OpenApiExample(
                name           = 'img_filter',
                value          = 'main,detail1,detail2',
                parameter_only = OpenApiParameter.QUERY,
                description    = "필요한 사진의 속성을 넣어주면 됩니다. \n\n 아무것도 넣어주지 않을 경우, 응답으로 상품에 속한 모든 사진을 받습니다."
                )]
            )
    ],
))
class ProductView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset           = Product.objects.all().prefetch_related('product_images')
    serializer_class   = ProductSerializer
    filter_backends    = [filters.DjangoFilterBackend]
    filterset_class    = ProductFilter
    
    def get_serializer_context(self):
        
        additional_context = {}

        # dyanamic field filtering
        want_fields     = self.request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))

        #img_filter
        img_filter = self.request.query_params.get('img_filter')
        if img_filter:
            # print(img_filter)
            # print("hi!")
            splited_img_filter = re.sub(",",":",img_filter).split(":") #자동으로 각 요소들이 str타입으로 리스트에  저장됨
            # print(splited_img_filter)
            ## list to dict 방법1
            it = iter(re.sub(",",":",img_filter).split(":"))
            img_filter = dict(zip(it,it))
            # print(img_filter)
            ## list to dict 방법2
            # lst = splited_img_filter
            # img_filter = {
            #     lst[i] : lst[i+1] for i in range(0,len(lst),2)
            # }
            additional_context['img_filter'] = img_filter
            print(additional_context)
        #context_update
        context = super().get_serializer_context()
        context.update(additional_context)
        
        return context
    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
    
        image_datas = []
        
        if request.FILES:
            s3_handler = S3Handler()
            for img in request.FILES:
                
                image_dict = {}
                
                request.data.pop(img)
                
                img_file = request.FILES.__getitem__(img)
                res_dict = s3_handler.upload(
                    file       = img_file,
                    Key        = f"backend/ProductImage/{str(uuid.uuid4())}",
                    field_name = f"{img}",
                )
                
                res_dict = iter(res_dict.values())
                
                image_dict['property'] = img
                image_dict['s3_path']  = res_dict.__next__()
                image_dict['img_url']  = res_dict.__next__()
                
                image_datas.append(image_dict)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,image_datas)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer,image_datas):
        user = self.request.user
        created = serializer.save()
        
        for image_dict in image_datas:
            print(image_dict)
            ProductImage.objects.create(product=created,**image_dict)
    

@extend_schema(methods=['PUT'], exclude=True)
@extend_schema_view(
    get = extend_schema(
        description = "## 설명 ## \n\n 상품 검색 \n\n <br/> \n\n ## 권한 ## \n\n 누구나(비회원도) 가능"),
    delete = extend_schema(
        description = "## 설명 ## \n\n 상품 삭제 \n\n 어드민 페이지에서 사용 \n\n <br/> \n\n ## 권한 ## \n\n 관리자만 가능"),
    patch = extend_schema(
        description = "## 설명 ## \n\n 상품 수정 \n\n 어드민 페이지에서 사용 \n\n <br/> \n\n ## 권한 ## \n\n 관리자만 가능",
        parameters=[
        OpenApiParameter(
            name        = 'img_delete',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "해당 상품의 이미지를 삭제할때 사용. [detail]라는 값을 보내줄 경우 해당 리뷰의 detail이 삭제되는 방식. []라는 값을 보낼 경우 아무기능도 하지 않음 ",
            examples    = [OpenApiExample(
                name           = 'img_delete',
                value          = 'ex) [main] , [], [main,detail2], [detail1,detail2]',
                parameter_only = OpenApiParameter.QUERY,
                description    = "[detail]와 같이 대괄호가 필수. 정해진 속성값외의 값이 대괄호 안에 들어올 경우 에러남"
                )]
            )],
        request=inline_serializer('product',{
        "product_name"         : serializers.CharField(),
        "category"             : serializers.CharField(),
        "price"                : serializers.FileField(),
        "description"          : serializers.FileField(),
        "optional_description" : serializers.FileField(),
        "is_active"            : serializers.FileField(),
        "main"                 : serializers.FileField(),
        "detail1"              : serializers.FileField(),
        "detail2"              : serializers.FileField(),
            }
        )
    )
) 
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset           = Product.objects.all()
    serializer_class   = ProductSerializer
    lookup_url_kwarg   = 'product_id'
    lookup_field       = 'id'
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        s3_handler = S3Handler()
        
        if request.FILES:
            
            image_datas = []
                
            for img in request.FILES:
                
                image_dict = {}
                
                if ProductImage.objects.filter(product=instance,property=img).exists():
                    productimage = ProductImage.objects.get(product=instance,property=img)
                    s3_handler.delete(productimage.s3_path)
                    productimage.delete()
                    
                img_file = request.FILES.__getitem__(img)
                
                res_dict = s3_handler.upload(
                file       = img_file,
                Key        = f"backend/ProductImage/{str(uuid.uuid4())}",
                field_name = f"{img}",
            )
                
                res_dict = iter(res_dict.values())
                
                image_dict['property'] = img
                image_dict['s3_path']  = res_dict.__next__()
                image_dict['img_url']  = res_dict.__next__()
                
                image_datas.append(image_dict)
                
            for image_dict in image_datas:
                ProductImage.objects.create(product=instance,**image_dict)

        if request.query_params.get('img_delete'):
            
            img_delete_list = request.query_params.get('img_delete').lstrip('[').rstrip(']').split(',')
            print(img_delete_list)
        
            if img_delete_list[0]:
                for img in img_delete_list:
                    ProductImage.objects.get(product=instance,property=img).delete()
            
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)    
            
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance   = self.get_object()
        product_images = instance.product_images.all()
        
        s3_handler = S3Handler()
        for image in product_images:
            s3_handler.delete(image.s3_path)
        
        product_images.delete()
        self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)