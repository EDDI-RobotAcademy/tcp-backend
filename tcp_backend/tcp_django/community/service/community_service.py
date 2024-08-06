from abc import ABC, abstractmethod


class CommunityService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def createCommunity(self, communityData):
        pass

    @abstractmethod
    def readCommunity(self, communityId):
        pass

    @abstractmethod
    def removeCommunity(self, communityId):
        pass

    @abstractmethod
    def updateCommunity(self, communityId, communityData):
        pass