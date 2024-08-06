from abc import ABC, abstractmethod


class ProfileRepository(ABC):
    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def findByNickname(self, nickname):
        pass

    @abstractmethod
    def create(self, nickname, email, gender, birthyear, account):
        pass

    @abstractmethod
    def findById(self, accountId):
        pass

    @abstractmethod
    def updateLastLogin(self, profile):
        pass

    @abstractmethod
    def update_login_history(self, profile):
        pass

    @abstractmethod
    def findByGender(self, id):
        pass