from abc import ABC, abstractmethod


class AccountRepository(ABC):
    @abstractmethod
    def create(self, loginType, roleType):
        pass

    @abstractmethod
    def findById(self, accountId):
        pass

    @abstractmethod
    def updateLastLogin(self, profile):
        pass

    @abstractmethod
    def withdrawAccount(self, account, withdrawReason):
        pass