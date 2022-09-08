from django.urls import path
from .views import FAQView,FAQDetailView,QnAView,QnADetailView,QnACommentView,QnACommenDetailView, NoticeView,NoticeDetailView

urlpatterns = [
    path('FAQ',FAQView.as_view(),name = 'faq'),
    path('FAQ/<int:faq_id>',FAQDetailView.as_view(),name = 'faq_detail'),
    path('QnA',QnAView.as_view(),name = 'qna'),
    path('QnA/<int:qna_id>',QnADetailView.as_view(),name = 'qna_detail'),
    path('QnA/<int:qna_id>/comments',QnACommentView.as_view(),name = 'qna_comment'),
    path('QnA/<int:qna_id>/comments/<int:comment_id>',QnACommenDetailView.as_view(),name = 'qna_comment_detail'),
    path('notices',NoticeView.as_view(),name = 'notice'),
    path('notices/<int:notice_id>',NoticeDetailView.as_view(),name = 'notice'),
]
