from abc import ABC, abstractmethod


class DocumentRepository(ABC):
    @abstractmethod
    def list(self):
        pass
