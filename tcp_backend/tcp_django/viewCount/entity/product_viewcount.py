from django.db import models
from product.entity.models import Product

class ProductViewCount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='view_count')
    count = models.PositiveIntegerField(default=0)

    def increment(self):
        self.count += 1
        self.save()

    class Meta:
        db_table = 'product_viewcount'
        app_label = 'viewCount'