from community.entity.models import Community
from community.repository.community_repository import CommunityRepository


class CommunityRepositoryImpl(CommunityRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Community.objects.all().order_by('regDate')

    def create(self, communityData):
        community = Community(**communityData)
        community.save()
        return community

    def findByCommunityId(self, communityId):
        return Community.objects.get(communityId=communityId)

    def deleteByCommunityId(self, communityId):
        community = Community.objects.get(communityId=communityId)
        community.delete()

    def update(self, community, communityData):
        for key, value in communityData.items():
            print(f"key: {key}, value: {value}")
            setattr(community, key, value)

        community.save()
        return community