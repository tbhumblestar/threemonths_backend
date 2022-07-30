from django.shortcuts           import get_object_or_404
from rest_framework             import generics
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated
from django_filters             import rest_framework as filters

from .models                    import Order, PackageOrder, OrderedProduct
from .serializers               import OrderSerializer, CafeOrderSerializer, CakeOrderSerializer, PackageOrderSerializer
from core.filters               import OrderFilter
from core.permissions           import OrderDetailPermission


detail_serializer_by_type = {
    "cafe"    : CafeOrderSerializer,
    "cake"    : CakeOrderSerializer,
    "package" : PackageOrderSerializer
}

class OrderView(generics.ListCreateAPIView):
    
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    filterset_class  = OrderFilter
    
    def create(self, request, *args, **kwargs):
        permission_classes = (IsAuthenticated,)
        order_data = {
            'title'         : request.data.pop('title',None),
            'type'          : request.data.pop('type',None),
            'customer_name' : request.data.pop('customer_name',None),
            'contact'       : request.data.pop('contact',None),
        }

        #want_fields
        additional_context = {}
        want_fields     = self.request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))
        
        
        serializer = self.get_serializer(data=order_data,context=additional_context)
        serializer.is_valid(raise_exception=True)
        
        detail_data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # response_data = {
        #     'common_data': serializer.data,
        #     'detail_data': detail_data
        # }

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def perform_create(self, serializer,**kwargs):
        user = self.request.user
        created_order = serializer.save(user = self.request.user)
        
        detail_serializer = detail_serializer_by_type[created_order.type](data=self.request.data)
        detail_serializer.is_valid(raise_exception=True)
        
        detail_serializer.save(order = created_order)
        return detail_serializer.data
    

class OrderDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (OrderDetailPermission,)
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    lookup_url_kwarg = 'order_id'
    lookup_field = 'id'