import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr = 'icontains')
    content = django_filters.CharFilter(lookup_expr = 'icontains')
    created_at = django_filters.DateFilter(field_name = 'created_at__date', lookup_expr= 'exact')
    created_at__gt = django_filters.DateFilter(field_name='created_at', lookup_expr= 'gt')
    created_at__gt = django_filters.DateFilter(field_name = 'created_at', lookup_expr= 'lt')
    created_at_range = django_filters.DateFromToRangeFilter(field_name = 'created_at')
    author__full_name = django_filters.CharFilter(lookup_expr='icontains')
    category__name = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        fields = [
            'title',
            'content',
            'category__name',
            'author__full_name',
            'created_at',

        ]