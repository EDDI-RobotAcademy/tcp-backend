from abc import ABC, abstractmethod


class DocumentRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def create(self, documentData):
        pass

    @abstractmethod
    def findByDocumentId(self, documentId):
        pass

    @abstractmethod
    def deleteByDocumentId(self, documentId):
        pass

    @abstractmethod
    def update(self, document, documentData):
        pass