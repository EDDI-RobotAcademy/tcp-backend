from django.db import models
from community.entity.models import Community

class CommunityViewCount(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='view_count')
    count = models.PositiveIntegerField(default=0)

    def increment(self):
        self.count += 1
        self.save()

    class Meta:
        db_table = 'community_viewcount'
        app_label = 'viewCount'