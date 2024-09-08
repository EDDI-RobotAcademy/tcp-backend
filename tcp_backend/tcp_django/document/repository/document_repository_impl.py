from document.entity.models import Document
from document.repository.document_repository import DocumentRepository


class DocumentRepositoryImpl(DocumentRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Document.objects.all().order_by('regDate')

    def create(self, documentData):
        document = Document(**documentData)
        document.save()
        return document

    def findByDocumentId(self, documentId):
        return Document.objects.get(documentId=documentId)

    def deleteByDocumentId(self, documentId):
        document = Document.objects.filter(documentId=documentId).first()
        if document:
            document.delete()
        else:
            raise Document.DoesNotExist(f'Document with id {documentId} does not exist.')

    def update(self, document, documentData):
        for key, value in documentData.items():
            print(f"key: {key}, value: {value}")
            setattr(document, key, value)

        document.save()
        return document