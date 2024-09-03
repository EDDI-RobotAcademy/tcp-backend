from abc import ABC, abstractmethod


class DocumentRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def create(self, documentData):
        pass
