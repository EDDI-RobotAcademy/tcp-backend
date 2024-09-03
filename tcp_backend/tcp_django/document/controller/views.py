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

    def create(self, request):
        # 파일 데이터를 포함한 새로운 데이터 생성
        data = request.data.copy()

        data['file'] = request.FILES.get('file')

        serializer = DocumentSerializer(data=data)
        # files 매개변수 제거

        if serializer.is_valid():
            document = self.documentService.createDocument(serializer.validated_data)
            return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def read(self, request, pk=None):
        document = self.documentService.readDocument(pk)
        if document:
            # view_count_document_service.increment_document_view_count(pk)
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        return Response({'status': 'error', 'message': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)


    def removeDocument(self, request, pk=None):
        self.documentService.removeDocument(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def modifyDocument(self, request, pk=None):
        document = self.documentService.readDocument(pk)
        serializer = DocumentSerializer(document, data=request.data, partial=True)

        if serializer.is_valid():
            updatedDocument = self.documentService.updateDocument(pk, serializer.validated_data)
            return Response(DocumentSerializer(updatedDocument).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)