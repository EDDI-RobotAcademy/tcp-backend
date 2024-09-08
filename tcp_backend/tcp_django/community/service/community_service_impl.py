from community.repository.community_repository_impl import CommunityRepositoryImpl
from community.service.community_service import CommunityService


class CommunityServiceImpl(CommunityService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__communityRepository = CommunityRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return self.__communityRepository.list()

    def createCommunity(self, communityData):
        return self.__communityRepository.create(communityData)

    def readCommunity(self, communityId):
        return self.__communityRepository.findByCommunityId(communityId)

    def removeCommunity(self, communityId):
        return self.__communityRepository.deleteByCommunityId(communityId)

    def updateCommunity(self, communityId, communityData):
        community = self.__communityRepository.findByCommunityId(communityId)
        return self.__communityRepository.update(community, communityData)

