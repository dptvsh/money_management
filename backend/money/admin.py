from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from money.models import (Category, OperationStatus, OperationType, Record,
                          SubCategory)


class RecordAdminForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data.get('category') and cleaned_data.get('operation_type')
                != cleaned_data.get('category').operation_type):
            raise ValidationError('Категория не соответствует типу операции')

        if (cleaned_data.get('subcategory') and cleaned_data.get('category')
                != cleaned_data.get('subcategory').category):
            raise ValidationError(
                'Подкатегория не принадлежит выбранной категории.',
            )

        return cleaned_data


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code',
    )


@admin.register(OperationStatus)
class OperationStatusAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code',
    )


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category',
    )


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name', 'operation_type')
    list_filter = ('operation_type',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    form = RecordAdminForm
    list_display = (
        'operation_date', 'status', 'operation_type',
        'category', 'subcategory', 'amount',
    )
    list_filter = ('status', 'operation_type', 'category', 'subcategory')
    search_fields = ('comment',)
    date_hierarchy = 'operation_date'
