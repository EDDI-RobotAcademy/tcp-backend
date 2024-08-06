from community.entity.models import Community
from viewCount.entity.community_viewcount import CommunityViewCount
from viewCount.repository.viewcount_community_repository import ViewCountCommunityRepository


class ViewCountCommunityRepositoryImpl(ViewCountCommunityRepository):

    def increment_community_view_count(self, communityId):
        try:
            community = Community.objects.get(pk=communityId)
            view_count, created = CommunityViewCount.objects.get_or_create(community=community)
            view_count.increment()
            return view_count.count
        except Community.DoesNotExist:
            return None