import django_filters
from . import models

class ItemFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.Item
        fields = ['item_type']