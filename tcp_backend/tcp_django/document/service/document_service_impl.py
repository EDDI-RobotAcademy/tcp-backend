from document.repository.document_repository_impl import DocumentRepositoryImpl
from document.service.document_service import DocumentService


class DocumentServiceImpl(DocumentService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__documentRepository = DocumentRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return self.__documentRepository.list()

    def createDocument(self, documentData):
        return self.__documentRepository.create(documentData)

    def readDocument(self, documentId):
        return self.__documentRepository.findByDocumentId(documentId)

    def removeDocument(self, documentId):
        return self.__documentRepository.deleteByDocumentId(documentId)

    def updateDocument(self, documentId, documentData):
        document = self.__documentRepository.findByDocumentId(documentId)
        return self.__documentRepository.update(document, documentData)

