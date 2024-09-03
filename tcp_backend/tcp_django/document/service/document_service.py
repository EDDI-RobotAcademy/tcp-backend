from abc import ABC, abstractmethod


class DocumentService(ABC):
    @abstractmethod
    def list(self):
        pass
