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
    
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["test"] = "test"
    #     # context["query_params"] = self.request.query_params
    #     return context

    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        additional_context = {}

        #dyanamic field filtering
        want_fields     = request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))

        #img_dict
        img_dict = request.query_params.get('img_dict')
        print("here!!!!")
        print("here!!!!")
        print(img_dict)
        print(type(img_dict))
        if img_dict:
            print("hi!")
            print("hi!")
            splited_img_dict = re.sub(",",":",img_dict).split(":") #자동으로 각 요소들이 str타입으로 리스트에  저장됨
            
            # #list to dict 방법1
            it = iter(re.sub(",",":",img_dict).split(":"))
            img_filter = dict(zip(it,it))
            print("img_filter : ",img_filter)
            
            #list to dict 방법2
            # lst = splited_img_dict
            # img_filter = {
            #     lst[i] : lst[i+1] for i in range(0,len(lst),2)
            # }

            additional_context['img_filter'] = img_filter
        
        print("here!!!!")
        print("here!!!!")
            
        #만들어진 context_dict를 serializer에 전달
       
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True,
                                            additional_context=additional_context)

            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True,
                                        additional_context=additional_context)
        return Response(serializer.data)
    
    
    

    # serializer = self.get_serializer(data=request.data)
    # serializer.context["customer_id"] = request.user.id
    # serializer.context["query_params"] = request.query_params

    # serializer.is_valid(raise_exception=True)
    # ...
    

    ##이걸 리스트로 바꿔서
    #리스트에서 리퀘스트쿼리파람스 > dict.update로 context에 넣어줌
    #listerializer에서 update를 시켜줌
    
    
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     serializer.context["customer_id"] = request.user.id
    #     serializer.context["query_params"] = request.query_params

    #     serializer.is_valid(raise_exception=True)
    #     ...