from django.db import models
from django.db.models import Count

class SubscriptionQuerySet(models.QuerySet):
    def ordered_count(self, field):
        return self.values_list(field)\
                   .annotate(count=Count(field))\
                   .order_by('-count')
