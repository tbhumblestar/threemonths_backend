from django.shortcuts           import get_object_or_404
from django.db                  import transaction
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
    "package" : PackageOrderSerializer,
    "cake"    : CakeOrderSerializer,
    "cafe"    : CafeOrderSerializer,
}

order_related_name_by_type = {
    "package" : 'packageorders',
    "cake"    : 'cakeorders',
    "cafe"    : 'cafeorders',
}


class OrderView(generics.ListCreateAPIView):
    
    permission_classes = (IsAuthenticated,)
    queryset           = Order.objects.all()
    serializer_class   = OrderSerializer
    filter_backends    = [filters.DjangoFilterBackend]
    filterset_class    = OrderFilter
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        #want_fields
        additional_context = {}
        want_fields     = self.request.query_params.get('fields')
        if want_fields:
            additional_context['want_fields'] = tuple(want_fields.split(','))
        
        
        serializer = self.get_serializer(data=request.data,context=additional_context)
        serializer.is_valid(raise_exception=True)
        
        detail_data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)


        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def perform_create(self, serializer,**kwargs):
        user = self.request.user
        created_order = serializer.save(user = self.request.user)
        
        detail_serializer = detail_serializer_by_type[created_order.type](data=self.request.data)
        detail_serializer.is_valid(raise_exception=True)
        
        detail_serializer.save(order = created_order)
        return detail_serializer.data
    

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (OrderDetailPermission,)
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    lookup_url_kwarg = 'order_id'
    lookup_field = 'id'
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        serializer.context['detail']   = True
        serializer.context['is_staff'] = request.user.is_staff
        return Response(serializer.data)
    
    
    def update(self, request, *args, **kwargs):
        
        partial    = kwargs.pop('partial', False)
        instance   = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer,instance,partial)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def perform_update(self, serializer, instance, partial):
        
        serializer.save()
        
        type = instance.type
        detail_instance = getattr(instance,order_related_name_by_type.get(type))
        detail_serializer = detail_serializer_by_type[type](instance=detail_instance,data=self.request.data,partial=partial)
        detail_serializer.is_valid(raise_exception=True)

        detail_serializer.save()