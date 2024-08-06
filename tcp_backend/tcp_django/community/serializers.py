from rest_framework import serializers
from community.entity.models import Community
from viewCount.entity.community_viewcount import CommunityViewCount

class CommunitySerializer(serializers.ModelSerializer):
    viewCount = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['communityId', 'title', 'writer', 'content', 'regDate', 'updDate', 'viewCount']
        read_only_fields = ['regDate', 'updDate', 'viewCount']

    def get_viewCount(self, obj):
        try:
            return obj.view_count.count
        except CommunityViewCount.DoesNotExist:
            return 0
