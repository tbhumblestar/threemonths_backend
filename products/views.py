import re

from rest_framework          import generics
from django_filters          import rest_framework as filters
from drf_spectacular.utils   import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes

from .models         import Product, IndependentImage
from .serializers    import IndependentImageSerializer, ProductSerializer
from core.filters    import IndependentImageFilter, ProductFilter
from core.decorators import query_debugger


class IndependentImageListView(generics.ListAPIView):
    queryset         = IndependentImage.objects.all()
    serializer_class = IndependentImageSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    filterset_class  = IndependentImageFilter

    @query_debugger
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
@extend_schema(
    description='Check Kakao access_token and return JWT_TOKEN',
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
    ],
)
class ProductListView(generics.ListAPIView):
    queryset         = Product.objects.filter(is_active = True).prefetch_related('product_images')
    serializer_class = ProductSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    filterset_class  = ProductFilter
    
    def get_serializer_context(self):
        
        additional_context = {}

        #dyanamic field filtering
        want_fields     = self.request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))

        #img_filter
        img_filter = self.request.query_params.get('img_filter')
        if img_filter:
            splited_img_filter = re.sub(",",":",img_filter).split(":") #자동으로 각 요소들이 str타입으로 리스트에  저장됨
            
            ## list to dict 방법1
            it = iter(re.sub(",",":",img_filter).split(":"))
            img_filter = dict(zip(it,it))
            
            ## list to dict 방법2
            # lst = splited_img_filter
            # img_filter = {
            #     lst[i] : lst[i+1] for i in range(0,len(lst),2)
            # }
            additional_context['img_filter'] = img_filter
        
        #need_count
        for_ordering    = self.request.query_params.get('for_ordering')
        if for_ordering == "True":
            additional_context["for_ordering"] = True
        
        #context_update
        context = super().get_serializer_context()
        context.update(additional_context)
        
        return context
    
    
@extend_schema(methods=['PUT','patch','delete'], exclude=True)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Product.objects.filter(is_active = True)
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'
    lookup_field = 'id'