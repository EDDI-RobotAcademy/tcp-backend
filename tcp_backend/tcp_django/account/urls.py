from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.controller.views import AccountView

router = DefaultRouter()
router.register(r'account', AccountView, basename='account')

urlpatterns = [
    path('', include(router.urls)),
    path('email-duplication-check',
         AccountView.as_view({'post': 'checkEmailDuplication'}), name='account-email-duplication-check'),
    path('nickname-duplication-check',
         AccountView.as_view({'post': 'checkNicknameDuplication'}), name='account-nickname-duplication-check'),
    path('register', AccountView.as_view({'post': 'registerAccount'}), name='register-account'),
    path('nickname', AccountView.as_view({'post': 'getNickname'}), name='nickname-account'),
    path('email', AccountView.as_view({'post': 'getEmail'}), name='email-account'),
    path('withdraw', AccountView.as_view({'post': 'withdrawAccount'}), name='withdraw-account'),
    path('gender', AccountView.as_view({'post': 'getGender'}), name='gender-account'),
    path('birthyear', AccountView.as_view({'post': 'getBirthyear'}), name='birthyear-account'),
    path('check-normal-login', AccountView.as_view({'post': 'checkNormalLogin'}), name='normal-login-check-account'),
]