from django.db.models           import Prefetch
from django.db                  import transaction
from requests import delete
from rest_framework             import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework             import serializers
from rest_framework.response    import Response
from rest_framework             import status
from drf_spectacular.utils      import extend_schema, extend_schema_view, inline_serializer, OpenApiExample, OpenApiParameter, OpenApiTypes
from django_filters             import rest_framework as filters
from datetime                   import datetime, timedelta
from django.db.models           import Case, When
from rest_framework.exceptions  import ValidationError

from .models          import Order, OrderedProduct, Review
from .serializers     import OrderSerializer, CafeOrderSerializer, CakeOrderSerializer, PackageOrderSerializer, UserOrderSerializer, ReviewSerializer
from core.filters     import OrderFilter
from core.permissions import OrderDetailPermission, OrderPermission, IsAuthenticatedOrReadOnly, IsAdminOrIsWriterOrReadOnly
from core.schema      import OrderSerializerSchema
from core.cores       import query_debugger, S3Handler

import uuid

detail_serializer_by_type = {
    "package" : PackageOrderSerializer,
    "cake"    : CakeOrderSerializer,
    "cafe"    : CafeOrderSerializer,
}

order_related_name_by_type = {
    "package" : 'packageorders',
    "cake"    : 'cakeorders',
    "cafe"    : 'cafeorders',
}

@extend_schema(
    request   = OrderSerializerSchema,
    responses = OrderSerializerSchema,
)
class OrderView(generics.ListCreateAPIView):
    
    permission_classes = (OrderPermission,)
    queryset           = Order.objects.all().\
        select_related('cafeorders','cakeorders','packageorders','cakeorders__product').\
        prefetch_related(Prefetch('packageorders__orderedproducts',queryset=OrderedProduct.objects.select_related('product')))

        
    serializer_class   = OrderSerializer
    filter_backends    = [filters.DjangoFilterBackend]
    filterset_class    = OrderFilter

    
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        #want_fields
        additional_context = {}
        want_fields        = self.request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))
        
        
        serializer  = self.get_serializer(data=request.data,context=additional_context)
        serializer.is_valid(raise_exception=True)
        
        detail_data = self.perform_create(serializer)
        headers     = self.get_success_headers(serializer.data)


        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def perform_create(self, serializer,**kwargs):
        user = self.request.user
        created_order = serializer.save(user = self.request.user)
        
        detail_serializer = detail_serializer_by_type[created_order.type](data=self.request.data)
        detail_serializer.is_valid(raise_exception=True)
        
        detail_serializer.save(order = created_order)
        return detail_serializer.data
    
@extend_schema(methods=['PUT'], exclude=True)
@extend_schema_view(
    get    = extend_schema(
        description = "## 권한 ## \n\n 작성자또는 관리자가 아니면 조회할 수 없음",
        responses   = {200 : OrderSerializerSchema}),
    patch  = extend_schema(
        description = "## 권한 ## \n\n 관리자는 언제든 수정 가능 \n\n 작성자는 status가 not_confirmed 일때만 수정 가능 <br><br/>  \n\n ## 수정할 수 있는 필드 ## \n\n type필드를 제외한 모든 필드",
        responses   = {200 : OrderSerializerSchema},
        request     = OrderSerializerSchema,
        examples         = [
        OpenApiExample(
            name         = 'package_order',
            description  = 'type을 제외한 모든 필드 수정 가능',
            request_only = True,
            value        = {
                "title"                  : "test",
                "customer_name"          : "tester",
                "contact"                : "010-0000-0000",
                "additional_explanation" : "test_explanation",
                "status"                 : "not_confirmed",
                "delivery_location"      : "test_location",
                "delivery_date"          : "2022-10-10",
                "purpose"                : "testasd",
                "orderedproducts"        : [
                    {
                        "product_id":4,
                        "buying":"True"
                    },
                    {
                        "product_id":8,
                        "buying":"True"
                    }
                ]
            },
        ),
        OpenApiExample(
            name         = 'cake_order',
            description  = 'type을 제외한 모든 필드 수정 가능',
            request_only = True,
            value        = {
                "title"                  : "testingasdsad",
                "customer_name"          : "tester",
                "contact"                : "010-0000-0000",
                "additional_explanation" : "test_explanation",
                "status"                 : "not_confirmed",
                "product_id"             : 13,
                "want_pick_up_date"      : "2022-10-15",
                "superdubaduib"          : "asdasdasd",
                "count"                  : 3
},
        ),
        OpenApiExample(
            name         = 'cafe_order',
            description  = 'type을 제외한 모든 필드 수정 가능',
            request_only = True,
            value        = {
                "title"                      :  "test",
                "customer_name"              :  "tester",
                "contact"                    :  "010-0000-0000",
                "additional_explanation"     :  "test_explanation",
                "status"                     : "not_confirmed",
                "cafename"                   :  "testcafe",
                "cafe_owner_name"            : "test_owner",
                "corporate_registration_num" : "kkk",
                "cafe_location"              : "test_location",
                "product_explanation"        : "asdasdasd"
},
        ),
        OpenApiExample(
            name          = 'package_order_response',
            response_only = True,
            value         = {
                "id"                     : 342,
                "type"                   : "package",
                "title"                  : "test",
                "customer_name"          : "tester",
                "contact"                : "010-0000-0000",
                "status"                 : "not_confirmed",
                "additional_explanation" : None,
                "created_at"             : "2022-08-08T03:40:58.554790",
                "updated_at"             : "2022-08-08T03:40:58.554824",
                "packageorders"          : {
                    "id"                : 182,
                    "delivery_location" : "test_location",
                    "delivery_date"     : "2022-10-10",
                    "is_packaging"      : None,
                    "purpose"           : "testasdasdfgasdasdasdasdasdasdsad",
                    "orderedproducts"   : [
                        {
                            "product_id"   : 4,
                            "buying"       : True,
                            "product_name" : "플레인 휘낭시에"
                        },
                        {
                            "product_id"    : 8,
                            "buying"        : True,
                            "product_name"  : "둘세 마들렌"
                        }
                    ]
                }
}
        ),                
        OpenApiExample(
            name          ='cake_order_response',
            response_only = True,
            value         = {
                "id"                     : 346,
                "type"                   : "cake",
                "title"                  : "testingasdsad",
                "customer_name"          : "tester",
                "contact"                : "010-0000-0000",
                "status"                 : "not_confirmed",
                "additional_explanation" : None,
                "created_at"             : "2022-08-08T04:12:07.160059",
                "updated_at"             : "2022-08-08T04:12:07.160088",
                "cakeorders"             : {
                    "id"                : 65,
                    "product_id"        : 16,
                    "product_name"      : "시즌 케이크(딸기)",
                    "want_pick_up_date" : "2022-10-15",
                    "count"             : 3
                }
            },
        ),                
        OpenApiExample(
            name          ='cafe_order_response',
            response_only = True,
            value         = {
                "id"                     : 347,
                "type"                   : "cafe",
                "title"                  : "test",
                "customer_name"          : "tester",
                "contact"                : "010-0000-0000",
                "status"                 : "not_confirmed",
                "additional_explanation" : None,
                "created_at"             : "2022-08-08T04:13:11.779439",
                "updated_at"             : "2022-08-08T04:13:11.779466",
                "cafeorders"             : {
                    "id"                         : 48,
                    "cafename"                   : "testcafe",
                    "cafe_owner_name"            : "test_owner",
                    "corporate_registration_num" : "kkk",
                    "cafe_location"              : "test_location",
                    "product_explanation"        : "asdasdasd"
                }
            }
        ),                
                    ]),
    delete = extend_schema(
        description = "## 권한 ## \n\n 관리자는 언제든 삭제 가능 \n\n 작성자는 status가 not_confirmed 일때만 삭제 가능 <br><br/>",
    )
)
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (OrderDetailPermission,)
    queryset           = Order.objects.all().\
        select_related('cafeorders','cakeorders','packageorders','cakeorders__product').\
        prefetch_related(Prefetch('packageorders__orderedproducts',queryset=OrderedProduct.objects.select_related('product')))

    serializer_class   = OrderSerializer
    filter_backends    = [filters.DjangoFilterBackend]
    lookup_url_kwarg   = 'order_id'
    lookup_field       = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        serializer.context['detail']   = True
        serializer.context['is_staff'] = request.user.is_staff
        return Response(serializer.data)
    
    
    def update(self, request, *args, **kwargs):
        
        partial    = kwargs.pop('partial', False)
        instance   = self.get_object()
        
        #detial form
        type              = instance.type
        detail_instance   = getattr(instance,order_related_name_by_type.get(type))
        detail_serializer = detail_serializer_by_type[type](instance=detail_instance,data=self.request.data,partial=partial)
        detail_serializer.is_valid(raise_exception=True)
        detail_serializer.save()
        
        #다시해줘야 함. 그래야 detail폼이 반영된 order이 들고와지고, serializer.data에 디테일폼의 변경된 내용이 담길 수 잇음
        instance   = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


valid_order_date = datetime.now() - timedelta(days=60)

@extend_schema_view(
    get = extend_schema(
        description = "## 권한 ## \n\n 로그인 햇을 경우 조회 가능 \n\n\n\n ## 목적 ## \n\n Review를 작성하기 위해 사용자가 주문했던 order 리스트를 조회 \n\n\n\n ## 조회되는 리스트 기준 ## \n\n -현재 요청을 보낸 유저의 Order \n\n -Type이 Packge 또는 Cake(Cafe 제외) \n\n -status가 completed \n\n -유저의 리뷰가 존재하지 않음 \n\n -날짜(cake:want_pick_up_date / PackageOrder:delivery_Date)가 오늘보다 60일 이내일 것 \n\n\n\n ## 특이사항 ## \n\n 지금은 테스트를 위하여 status가 completed가 아니여도 조회되도록 해두었음",
    )
)
class UserOrderListView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class   = UserOrderSerializer
    
    """
    -현재 요청을 보낸 유저의 & Type이 Packge or Cake & status가 completed & review데이터가 없는 & 날짜(cake:want_pick_up_date / PackageOrder:delivery_Date)가 오늘보다 60일 이내
    """
    def get_queryset(self):
        
        user = self.request.user
        
        if self.request.data.get('all') == "True":
            queryset = Order.objects.all(user=user)
            return queryset
    
        queryset = Order.objects.\
            filter(type__in=['cake','package']).\
                select_related('cafeorders','cakeorders','reviews').\
                annotate(dates=Case(
                    When(type='package',then='packageorders__delivery_date'),
                    When(type='cake',then='cakeorders__want_pick_up_date'))).\
                        filter(
                            dates__gte      = valid_order_date,
                            reviews__isnull = True,
                            # status          = 'completed',
                            user            = user)
        return queryset

@extend_schema_view(
    get = extend_schema(
        description = "## 권한 ## \n\n 누구나 조회 가능",
        parameters=[
        OpenApiParameter(
            name        = 'user_review',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "특정 유저의 모든 리뷰를 모아보고 싶을 때 사용 \n\n True를 줄 경우, 요청을 보낸 유저의 모든 리뷰를 리스트로 보내줌",
            examples    = [OpenApiExample(
                name           = 'user_review',
                value          = 'ex) True',
                parameter_only = OpenApiParameter.QUERY,
                description    = "True 이외의 값을 줄 경우 작동하지 않음"
                )]
            ),
        OpenApiParameter(
            name        = 'type',
            type        = OpenApiTypes.STR,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "cake 또는 package의 모든 리뷰를 모아보고 싶을 때 사용 \n\n order의 타입(packageorder, cakeorder)이 일치하는 모든 리뷰를 가져옴",
            examples    = [OpenApiExample(
                name           = 'type',
                value          = 'ex) cake,package',
                parameter_only = OpenApiParameter.QUERY,
                description    = "cake, package이외의 값을 넣어줄 경우 속하는 카테고리가 없어서 응답되는 데이터가 없음"
                )]
            ),
        OpenApiParameter(
            name        = 'product_id',
            type        = OpenApiTypes.INT,
            location    = OpenApiParameter.QUERY,
            required    = False,
            description = "특정 케이크 상품의 모든 리뷰를 모아보고 싶을 때 사용 \n\n 케이크 상품의 product_id에 속하는 모든 리뷰를 리스트로 응답",
            examples    = [OpenApiExample(
                name           = 'product_id',
                value          = 'ex) 15',
                parameter_only = OpenApiParameter.QUERY,
                description    = "케이크 상품의 product_id를 넣어줘야 함"
                )]
            ),
    ],
    ),
    post = extend_schema(
        description = "## 권한 ## \n\n 로그인 해야 생성(Post) 가능 \n\n ## 제한 ## \n\n 하나의 Order에 대해 유저는 한번의 리뷰만 쓸 수 있음(삭제하고 다시 쓰는 건 가능)",
        request=inline_serializer('user',{
        "title"   : serializers.CharField(),
        "content" : serializers.CharField(),
        "order"   : serializers.IntegerField(),
        "img"     : serializers.FileField(),
    }
                                ),
    )
)
class ReviewView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class   = ReviewSerializer
    
    
    def get_queryset(self):
        
        query_dict = {}
        
        queryset = Review.objects.all().select_related('user')
        
        #마이페이지에서 user가 작성한 review만 모아보고 싶을 때
        if self.request.query_params.get('user_review') == "True":
            queryset = queryset.filter(user=self.request.user)
            return queryset
        
        
        #package review 혹은 특정 cake상품 review
        if self.request.query_params.get('product_id'):
            query_dict['order__type'] = 'cake'
            query_dict['order__cakeorders__product_id'] = self.request.query_params.get('product_id')
        elif self.request.query_params.get('type'):
            query_dict['order__type'] = self.request.query_params.get('type')
            
        
        queryset = queryset.filter(**query_dict)
        return queryset

    
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        
        order = request.data.get('order')
        if Review.objects.filter(user=self.request.user,order=order).exists():
            raise ValidationError("You have already written review for this order")
        
        
        img_dict = {}
        
        if request.FILES:
            s3_handler = S3Handler()
            for img in request.FILES:
                
                #getlist의 경우 여러장의 이미지를 하나의 키값으로 받을때 배열로 받는 메서드이고,
                #getitem의 경우 한장의 이미지가 하나의 키값에 존재할 때 사용할 수 있는 메서드이다.
                
                request.data.pop(img)
                
                img_data = request.FILES.__getitem__(img)
                res_dict = s3_handler.upload(
                    file = img_data,
                    Key  = f"backend/reviews/{str(uuid.uuid4())}",
                    field_name = 'img'
                    )
                
        img_dict.update(res_dict)
        
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,res_dict)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer,res_dict):
        user = self.request.user
        serializer.save(**res_dict,user=user)


@extend_schema(methods=['PUT'], exclude=True)
@extend_schema_view(
    get = extend_schema(
        description = "## 권한 ## \n\n 누구나(비회원도) 가능"),
    delete = extend_schema(
        description = "## 권한 ## \n\n 작성자, 관리자가 아니면 불가능"),
    patch = extend_schema(
        description = "## 권한 ## \n\n 작성자, 관리자가 아니면 불가능",
        request=inline_serializer('user',{
        "title"   : serializers.CharField(),
        "content" : serializers.CharField(),
        "order"   : serializers.IntegerField(),
        "img"     : serializers.FileField(),
    }
                                ),
    )
)
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrIsWriterOrReadOnly]
    serializer_class   = ReviewSerializer
    queryset           = Review.objects.all().select_related('user')
    lookup_url_kwarg   = 'review_id'
    lookup_field       = 'id'
    
    
    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        img_dict = {}        
        if request.FILES:
            
            s3_handler = S3Handler()
            for img in request.FILES:
                
                #getlist의 경우 여러장의 이미지를 하나의 키값으로 받을때 배열로 받는 메서드이고,
                #getitem의 경우 한장의 이미지가 하나의 키값에 존재할 때 사용할 수 있는 메서드이다.
                request.data.pop(img)
                s3_handler.delete(instance.img_s3_path)
                
                img_file = request.FILES.__getitem__(img)
                res_dict = s3_handler.upload(
                    file = img_file,
                    Key  = f"backend/reviews/{str(uuid.uuid4())}",
                    field_name = 'img'
                    )
            
            img_dict.update(res_dict)
                
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
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        s3_handler = S3Handler()
        s3_handler.delete(instance.img_s3_path)
        
        self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    