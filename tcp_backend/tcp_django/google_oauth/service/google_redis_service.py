from abc import ABC, abstractmethod

class GoogleRedisService(ABC):
    @abstractmethod
    def store_access_token(self, account_id, userToken):
        pass

    @abstractmethod
    def getValueByKey(self, key):
        pass

    @abstractmethod
    def deleteKey(self, key):
        pass