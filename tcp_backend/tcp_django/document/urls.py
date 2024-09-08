from django.urls import include, path
from rest_framework.routers import DefaultRouter

from document.controller.views import DocumentView

router = DefaultRouter()
router.register(r"document", DocumentView)

urlpatterns = [
    path("", include(router.urls)),
    path("register", DocumentView.as_view({"post": "create"}), name="document-register"),
    path("list/", DocumentView.as_view({"get": "list"}), name="document-list"),
    path("read/<int:pk>", DocumentView.as_view({"get": "read"}), name="document-read"),
    path("modify/<int:pk>", DocumentView.as_view({"put": "modifyDocument"}), name="document-modify"),
    path("delete/<int:pk>", DocumentView.as_view({"delete": "removeDocument"}), name="document-remove"),
]
