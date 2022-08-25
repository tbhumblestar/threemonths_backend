from django.urls import path
from .views import OrderView,OrderDetailView, UserOrderListView, ReviewView, ReviewDetailView

urlpatterns = [
    path('',OrderView.as_view(),name = 'order'),
    path('<int:order_id>',OrderDetailView.as_view(),name = 'order_detail'),
    path('userorders',UserOrderListView.as_view(),name = 'user_order'),
    path('reviews',ReviewView.as_view(),name = 'review'),
    path('reviews/<int:review_id>',ReviewDetailView.as_view(),name = 'review_detail'),
]
