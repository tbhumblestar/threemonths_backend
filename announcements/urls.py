from django.urls import path
from .views import FAQView,FAQDetailView,QnAView,QnADetailView,QnACommentView,QnACommenDetailView

urlpatterns = [
    path('FAQ',FAQView.as_view(),name = 'faq'),
    path('FAQ/<int:faq_id>',FAQDetailView.as_view(),name = 'faq_detail'),
    path('QnA',QnAView.as_view(),name = 'q_and_a'),
    path('QnA/<int:q_and_a_id>',QnADetailView.as_view(),name = 'q_and_a_detail'),
    path('QnA/<int:q_and_a_id>/comment',QnACommentView.as_view(),name = 'q_and_a_comment'),
    path('QnA/<int:q_and_a_id>/comment/<int:comment_id>',QnACommenDetailView.as_view(),name = 'q_and_a_comment_detail'),
]
