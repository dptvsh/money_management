from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api.filters import RecordFilter
from api.serializers import (CategorySerializer, OperationStatusSerializer,
                             OperationTypeSerializer, RecordSerializer,
                             SubCategorySerializer)
from money.models import (Category, OperationStatus, OperationType, Record,
                          SubCategory)


class CatalogViewSet(viewsets.ModelViewSet):
    """
    Базовый вьюсет для справочников с SlugField как PK.
    Поддерживает lookup_field = 'code' для всех операций.
    """

    lookup_field = 'code'
    lookup_url_kwarg = 'code'


class RecordViewSet(viewsets.ModelViewSet):
    """Вьюсет записей."""

    queryset = Record.objects.select_related(
        'status', 'operation_type', 'category', 'subcategory'
    ).order_by('-operation_date')
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RecordFilter

    def get_object(self):
        if self.kwargs.get('pk').isdigit():
            return super().get_object()
        return Record.objects.get(code=self.kwargs['pk'])


class OperationTypeViewSet(CatalogViewSet):
    """Вьюсет типов операций."""

    queryset = OperationType.objects.all().order_by('name')
    serializer_class = OperationTypeSerializer


class OperationStatusViewSet(CatalogViewSet):
    """Вьюсет статусов операций."""

    queryset = OperationStatus.objects.all().order_by('name')
    serializer_class = OperationStatusSerializer


class CategoryViewSet(CatalogViewSet):
    """Вьюсет категорий."""

    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        operation_type = self.request.query_params.get('operation_type')
        if operation_type:
            queryset = queryset.filter(operation_type__code=operation_type)
        return queryset


class SubCategoryViewSet(CatalogViewSet):
    """Вьюсет подкатегорий."""

    serializer_class = SubCategorySerializer

    def get_queryset(self):
        queryset = SubCategory.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__code=category)
        return queryset
