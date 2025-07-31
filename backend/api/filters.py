from django_filters import rest_framework as filters

from money.models import Record


class RecordFilter(filters.FilterSet):
    operation_date = filters.DateFromToRangeFilter(
        field_name='operation_date',
        label='Диапазон дат (YYYY-MM-DD)',
    )
    category = filters.CharFilter(
        field_name='category__code',
        label='Фильтр по коду категории'
    )

    class Meta:
        model = Record
        fields = {
            'status': ['exact'],
            'operation_type': ['exact'],
            'subcategory': ['exact'],
        }
