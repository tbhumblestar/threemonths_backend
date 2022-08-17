from pymysql                 import NULL
from django.db.models        import Prefetch
from django.db               import transaction
from rest_framework          import generics
from rest_framework          import serializers
from rest_framework.response import Response
from rest_framework          import status
from drf_spectacular.utils   import extend_schema, extend_schema_view, inline_serializer, OpenApiExample, PolymorphicProxySerializer
from django_filters          import rest_framework as filters

from .models          import Order, PackageOrder, OrderedProduct
from .serializers     import OrderSerializer, CafeOrderSerializer, CakeOrderSerializer, PackageOrderSerializer
from core.filters     import OrderFilter
from core.permissions import OrderDetailPermission, OrderPermission
from core.schema      import OrderSerializerSchema
from core.decorators  import query_debugger


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
                "additional_explanation" : NULL,
                "created_at"             : "2022-08-08T03:40:58.554790",
                "updated_at"             : "2022-08-08T03:40:58.554824",
                "packageorders"          : {
                    "id"                : 182,
                    "delivery_location" : "test_location",
                    "delivery_date"     : "2022-10-10",
                    "is_packaging"      : NULL,
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
                "additional_explanation" : NULL,
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
                "additional_explanation" : NULL,
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

