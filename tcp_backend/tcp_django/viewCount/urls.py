from django.urls import include, path
from rest_framework.routers import DefaultRouter
from viewCount.controller.views import ViewCountView

router = DefaultRouter()
router.register(r'view-count', ViewCountView, basename='view-count')

urlpatterns = [
    path('', include(router.urls)),
]
