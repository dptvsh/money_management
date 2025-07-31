from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, OperationStatusViewSet,
                    OperationTypeViewSet, RecordViewSet, SubCategoryViewSet)

router = DefaultRouter()
router.register(r'records', RecordViewSet)
router.register(r'operation_types', OperationTypeViewSet)
router.register(r'operation_statuses', OperationStatusViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')

urlpatterns = [
    path('', include(router.urls)),
]
