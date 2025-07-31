from django.db import models
from django.utils.timezone import now

from money.constants import MAX_LENGTH_CODE_NAME, MAX_LENGTH_NAME


class OperationType(models.Model):
    name = models.CharField(
        verbose_name='Название типа операции',
        max_length=MAX_LENGTH_NAME,
        unique=True,
    )
    code = models.SlugField(
        verbose_name='Идентификатор типа операции',
        max_length=MAX_LENGTH_CODE_NAME,
        unique=True,
    )

    class Meta:
        verbose_name = 'тип операции'
        verbose_name_plural = 'Типы операции'

    def __str__(self):
        return self.name


class OperationStatus(models.Model):
    name = models.CharField(
        verbose_name='Название статуса операции',
        max_length=MAX_LENGTH_NAME,
        unique=True,
    )
    code = models.SlugField(
        verbose_name='Идентификатор статуса операции',
        max_length=MAX_LENGTH_CODE_NAME,
        unique=True,
    )

    class Meta:
        verbose_name = 'статус операции'
        verbose_name_plural = 'Статусы операции'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=MAX_LENGTH_NAME,
    )
    operation_type = models.ForeignKey(
        OperationType, on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип операции',
        to_field='code',
    )
    code = models.SlugField(
        verbose_name='Идентификатор категории',
        max_length=MAX_LENGTH_CODE_NAME,
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'operation_type'],
                name='unique_type_name',
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.operation_type})"


class SubCategory(models.Model):
    name = models.CharField(
        verbose_name='Название подкатегории',
        max_length=MAX_LENGTH_NAME,
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория',
        to_field='code',
    )
    code = models.SlugField(
        verbose_name='Идентификатор подкатегории',
        max_length=MAX_LENGTH_CODE_NAME,
        unique=True,
    )

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_category_name',
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Record(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Дата создания записи',
        auto_now_add=True,
    )
    operation_date = models.DateField(
        verbose_name='Дата совершения операции',
        default=now,
    )
    status = models.ForeignKey(
        OperationStatus, on_delete=models.PROTECT,
        verbose_name='Статус операции',
        related_name='records_by_status',
        to_field='code',
    )
    operation_type = models.ForeignKey(
        OperationType, on_delete=models.PROTECT,
        verbose_name='Тип операции',
        related_name='records_by_type',
        to_field='code',
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='records_by_category',
        to_field='code',
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT,
        verbose_name='Подкатегория',
        related_name='records_by_subcategory',
        to_field='code',
    )
    amount = models.DecimalField(
        verbose_name='Сумма',
        max_digits=12, decimal_places=2,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True, null=True,
    )

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'Записи'
        ordering = ('-operation_date',)

    def __str__(self):
        return f"{self.operation_date} - {self.amount} ({self.status})"
