from django.shortcuts import render
from .models import Order, PackageOrder, OrderedProduct
from .serializers import OrderSerializer, CafeOrderSerializer, CakeOrderSerializer, PackageOrderSerializer
from core.filters import OrderFilter
# Create your views here.

from rest_framework             import generics
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated
from django_filters             import rest_framework as filters

import re


serializer_by_type = {
    "cafe"    : CafeOrderSerializer,
    "cake"    : CakeOrderSerializer,
    "package" : PackageOrderSerializer
}


class OrderListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, )
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    filterset_class  = OrderFilter
    
    
    
    def create(self, request, *args, **kwargs):
        
        order_data = {
            'title':request.data.pop('title',None),
            'type':request.data.pop('type',None),
            'customer_name':request.data.pop('customer_name',None),
            'contact':request.data.pop('contact',None),
        }

        #want_fields
        additional_context = {}
        want_fields     = self.request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))
        
        
        
        serializer = self.get_serializer(data=order_data,context=additional_context)
        serializer.is_valid(raise_exception=True)
        
        detail_form_data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        create_response_data = {
            'common_data' : serializer.data,
            'detail' : detail_form_data
        }
        
        return Response(create_response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        user = self.request.user
        created_order = serializer.save(user = self.request.user)

        print("self.request.data : ",self.request.data)
        
        detail_serializer = serializer_by_type[created_order.type](data=self.request.data)
        detail_serializer.is_valid(raise_exception=True)
        detail_serializer.save(order = created_order)
        return detail_serializer.data