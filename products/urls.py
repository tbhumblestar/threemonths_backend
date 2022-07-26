from django.urls import path
from .views import IndependentImageListView, ProductListView, ProductDetailView

urlpatterns = [
    path('independentimages',IndependentImageListView.as_view(),name = 'IndependentImage'),
    path('',ProductListView.as_view(),name ='ProductList'),
    path('<int:product_id>',ProductDetailView.as_view(),name='ProductDetail')
]
