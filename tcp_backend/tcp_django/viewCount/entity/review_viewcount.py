from django.db import models
from review.entity.models import Review

class ReviewViewCount(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='view_count')
    count = models.PositiveIntegerField(default=0)

    def increment(self):
        self.count += 1
        self.save()

    class Meta:
        db_table = 'review_viewcount'
        app_label = 'viewCount'