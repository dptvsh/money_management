from django.utils.dateparse import parse_date
from rest_framework import serializers

from money.constants import MAX_AMOUNT, MIN_AMOUNT
from money.models import (Category, OperationStatus, OperationType, Record,
                          SubCategory)


class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = (
            'name', 'code',
        )


class OperationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationStatus
        fields = (
            'name', 'code',
        )


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = (
            'name', 'category', 'code',
        )


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(
        many=True,
        read_only=True,
        source='categories',
    )

    class Meta:
        model = Category
        fields = (
            'name', 'operation_type', 'code', 'subcategories',
        )


class RecordSerializer(serializers.ModelSerializer):
    operation_date = serializers.CharField()
    status = serializers.SlugRelatedField(
        slug_field='code',
        queryset=OperationStatus.objects.all()
    )
    operation_type = serializers.SlugRelatedField(
        slug_field='code',
        queryset=OperationType.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Category.objects.all()
    )
    subcategory = serializers.SlugRelatedField(
        slug_field='code',
        queryset=SubCategory.objects.all()
    )

    class Meta:
        model = Record
        fields = (
            'created_at', 'operation_date', 'status', 'operation_type',
            'category', 'subcategory', 'amount', 'comment',
        )
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'operation_date': {'help_text': 'Формат: ДД.ММ.ГГГГ'}
        }

    def validate_operation_date(self, value):
        try:
            day, month, year = map(int, value.split('.'))
            return f"{year}-{month:02d}-{day:02d}"
        except (ValueError, AttributeError):
            raise serializers.ValidationError('Используйте формат ДД.ММ.ГГГГ')

    def validate(self, data):
        if data['category'].operation_type != data['operation_type']:
            raise serializers.ValidationError(
                'Выбранная категория не относится к выбранному типу операции.',
            )

        if data['subcategory'].category != data['category']:
            raise serializers.ValidationError(
                'Выбранная подкатегория не относится к выбранной категории.',
            )

        if data['amount'] <= MIN_AMOUNT:
            raise serializers.ValidationError(
                'Сумма должна быть положительной.',
            )
        elif data['amount'] > MAX_AMOUNT:
            raise serializers.ValidationError(
                'Вы вышли за пределы, уменьшите сумму.',
            )

        return data

    def to_representation(self, instance):
        """Преобразуем обратно в дд.мм.гггг при выводе"""
        data = super().to_representation(instance)
        if 'operation_date' in data:
            date_obj = parse_date(data['operation_date'])
            data['operation_date'] = date_obj.strftime('%d.%m.%Y')
        return data
