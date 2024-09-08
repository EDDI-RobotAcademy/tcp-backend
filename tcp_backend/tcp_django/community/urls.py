from django.urls import include, path
from rest_framework.routers import DefaultRouter

from community.controller.views import CommunityView

router = DefaultRouter()
router.register(r"community", CommunityView)

urlpatterns = [
    path("", include(router.urls)),
    path("register", CommunityView.as_view({"post": "create"}), name="community-register"),
    path("list/", CommunityView.as_view({"get": "list"}), name="community-list"),
    path("read/<int:pk>", CommunityView.as_view({"get": "read"}), name="community-read"),
    path("modify/<int:pk>", CommunityView.as_view({"put": "modifyCommunity"}), name="community-modify"),
    path("delete/<int:pk>", CommunityView.as_view({"delete": "removeCommunity"}), name="community-remove"),
]
