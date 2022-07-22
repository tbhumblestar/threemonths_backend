from rest_framework          import generics
from rest_framework.response import Response
from django_filters          import rest_framework as filters


from .models      import Product,ProductImage, IndependentImage
from .serializers import IndependentImageSerializer, ProductSerializer
from core.filters import IndependentImageFilter, ProductFilter

# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()

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
        context = super().get_serializer_context()
        context["test"] = "test"
        # context["query_params"] = self.request.query_params
        return context


    # serializer = self.get_serializer(data=request.data)
    # serializer.context["customer_id"] = request.user.id
    # serializer.context["query_params"] = request.query_params

    # serializer.is_valid(raise_exception=True)
    # ...