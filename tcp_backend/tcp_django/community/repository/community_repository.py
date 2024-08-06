from abc import ABC, abstractmethod


class CommunityRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def create(self, communityData):
        pass

    @abstractmethod
    def findByCommunityId(self, communityId):
        pass

    @abstractmethod
    def deleteByCommunityId(self, communityId):
        pass

    @abstractmethod
    def update(self, community, communityData):
        pass