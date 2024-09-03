from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from document.entity.models import Document
from document.serializers import DocumentSerializer
from document.service.document_service_impl import DocumentServiceImpl

class DocumentView(viewsets.ViewSet):
    queryset = Document.objects.all()
    documentService = DocumentServiceImpl.getInstance()

    def list(self, request):
        documentList = self.documentService.list()
        print('documentList:', documentList)
        serializer = DocumentSerializer(documentList, many=True)
        print('serialized documentList:', serializer.data)
        return Response(serializer.data)
