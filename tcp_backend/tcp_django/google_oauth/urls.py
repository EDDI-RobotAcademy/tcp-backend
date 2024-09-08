from django.urls import path, include

from rest_framework.routers import DefaultRouter

from google_oauth.controller.views import GoogleOauthView

router = DefaultRouter()
router.register(r'google_oauth', GoogleOauthView, basename='google_oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('google', GoogleOauthView.as_view({'get': 'googleOauthURI'}), name='get-google-oauth-uri'),
    path('google/access-token', GoogleOauthView.as_view({'post': 'googleAccessTokenURI'}), name='get-google-access-token-uri'),
    path('google/user-info', GoogleOauthView.as_view({'post': 'googleUserInfoURI'}), name='get-google-user-info-uri'),
    path('redis-access-token', GoogleOauthView.as_view({'post': 'redisAccessToken'}), name='redis-access-token'),
    path('logout', GoogleOauthView.as_view({'post': 'dropRedisTokenForLogout'}), name='drop-redis-token-for-logout')
]