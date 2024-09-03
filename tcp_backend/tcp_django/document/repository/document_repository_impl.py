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
