from rest_framework          import generics
from rest_framework.response import Response
from django_filters          import rest_framework as filters


from .models      import Product,ProductImage, IndependentImage
from .serializers import IndependentImageSerializer, ProductSerializer
from core.filters import IndependentImageFilter, ProductFilter

import re


class IndependentImageListView(generics.ListAPIView):
    queryset         = IndependentImage.objects.all()
    serializer_class = IndependentImageSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    filterset_class  = IndependentImageFilter
    

class ProductListView(generics.ListAPIView):
    queryset         = Product.objects.filter(is_active = True)
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
        need_count     = self.request.query_params.get('need_count')
        if need_count == "True":
            additional_context["need_count"] = True
        
        #context_update
        context = super().get_serializer_context()
        context.update(additional_context)
        
        return context
    
class ProductDetailView(generics.ListAPIView):
    queryset         = Product.objects.filter(is_active = True)
    serializer_class = ProductSerializer