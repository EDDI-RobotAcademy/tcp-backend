from abc import ABC, abstractmethod


class AccountService(ABC):
    @abstractmethod
    def checkEmailDuplication(self, email):
        pass

    @abstractmethod
    def checkNicknameDuplication(self, nickname):
        pass

    @abstractmethod
    def registerAccount(self, loginType, roleType, nickname, email, password, salt, gender, birthyear):
        pass

    @abstractmethod
    def findAccountByEmail(self, email):
        pass
    
    @abstractmethod
    def withdrawAccount(self, accountId, withdrawReason):
        pass