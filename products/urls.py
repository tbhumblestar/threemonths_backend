from django.urls import path
from .views import IndependentImageListView, ProductListView

urlpatterns = [
    path('independentimages',IndependentImageListView.as_view(),name = 'IndependentImage'),
    path('',ProductListView.as_view(),name ='Product')
]
