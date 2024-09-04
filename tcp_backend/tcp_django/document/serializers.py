from rest_framework import serializers
from document.entity.models import Document

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['documentId', 'title', 'writer', 'file', 'content', 'regDate', 'updDate']
        read_only_fields = ['regDate', 'updDate']


