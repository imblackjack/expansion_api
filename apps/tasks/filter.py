
import django_filters
from .models import Tasks


class TaksFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    name = django_filters.CharFilter(field_name="creator", lookup_expr='icontains')
    name = django_filters.CharFilter(field_name="playbook", lookup_expr='icontains')

    class Meta:
        model = Tasks
        fields = ['name', 'creator', 'playbook']
