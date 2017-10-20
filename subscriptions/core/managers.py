from django.db import models
from django.db.models import Count


class SubscriptionQuerySet(models.QuerySet):
    def values_list_count(self, field):
        return self.values_list(field)\
                   .annotate(count=Count(field))

    def values_list_count_ordered(self, field):
        return self.values_list_count(field).order_by('-count')
