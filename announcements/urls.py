from django.urls import path
from .views import FAQView,FAQDetailView,QnAView,QnADetailView,QnACommentView,QnACommenDetailView, NoticeAPIView

urlpatterns = [
    path('FAQ',FAQView.as_view(),name = 'faq'),
    path('FAQ/<int:faq_id>',FAQDetailView.as_view(),name = 'faq_detail'),
    path('QnA',QnAView.as_view(),name = 'qna'),
    path('QnA/<int:qna_id>',QnADetailView.as_view(),name = 'qna_detail'),
    path('QnA/<int:qna_id>/comments',QnACommentView.as_view(),name = 'qna_comment'),
    path('QnA/<int:qna_id>/comments/<int:comment_id>',QnACommenDetailView.as_view(),name = 'qna_comment_detail'),
    path('notices',NoticeAPIView.as_view(),name = 'notice'),
]
