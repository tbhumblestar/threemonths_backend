from django.shortcuts import render
from .models import Order, PackageOrder, OrderedProductsInPackage
from .serializers import OrderSerializer
from core.filters import OrderFilter
# Create your views here.

from rest_framework          import generics
from rest_framework.response import Response
from rest_framework          import status
from rest_framework.permissions import IsAuthenticated
from django_filters          import rest_framework as filters


import re

class OrderListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, )
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends  = [filters.DjangoFilterBackend]
    filterset_class  = OrderFilter
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = self.request.user)