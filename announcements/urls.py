from django.urls import path
from .views import FAQView,FAQDetailView

urlpatterns = [
    path('',FAQView.as_view(),name = 'faq'),
    path('<int:faq_id>',FAQDetailView.as_view(),name = 'faq_detail'),
]
