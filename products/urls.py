from django.urls import path
from .views import IndependentImageListView, ProductView, ProductDetailView

urlpatterns = [
    path('independentimages',IndependentImageListView.as_view(),name = 'IndependentImage'),
    path('',ProductView.as_view(),name ='ProductListCreate'),
    path('<int:product_id>',ProductDetailView.as_view(),name='ProductDetail')
]
