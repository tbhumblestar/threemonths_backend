from django.urls import path
from .views import KaKaoLoginView,KaKaoLogOutView,RunSMSAuthView, MatchEmailAndContactNumView, GetEmailByContactNumView, SetNewPWView, SiteSignUpView, CheckSMSAuthView


urlpatterns = [
    #기능이 다 정해지면 auth라는 클래스에 맵퍼함수를 만들어서 한번에 처리할 수 있도록 해볼 것
    path('kakaologin',KaKaoLoginView.as_view(),name='kakaologin'),
    path('kakaologout',KaKaoLogOutView.as_view(),name='kakaologout'),
    path('runsmsauth',RunSMSAuthView.as_view(),name='runsmsauth'),
    path('checksmsauth',CheckSMSAuthView.as_view(),name='checksmsauth'),
    path('matchemailandcontactnum',MatchEmailAndContactNumView.as_view(),name='matchemailandcontactnum'),
    path('getemailbycontactnumview',GetEmailByContactNumView.as_view(),name='getemailbycontactnumview'),
    path('setnewpw',SetNewPWView.as_view(),name='setnewpw'),
    path('sitesignup',SiteSignUpView.as_view(),name='sitesignup'),
]
