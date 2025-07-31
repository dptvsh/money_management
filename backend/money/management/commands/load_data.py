import csv

from django.core.management.base import BaseCommand

from money.models import Category, OperationStatus, OperationType, SubCategory


class Command(BaseCommand):
    help = 'Импорт начальных данных из CSV файла.'

    def import_operation_statuses(self):
        with open('static/data/operation_status.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, code = row
                OperationStatus.objects.get_or_create(
                    name=name,
                    code=code,
                )
        self.stdout.write('Статусы операций успешно импортированы.')

    def import_operation_types(self):
        with open('static/data/operation_type.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, code = row
                OperationType.objects.get_or_create(
                    name=name,
                    code=code,
                )
        self.stdout.write('Типы операций успешно импортированы.')

    def import_categories(self):
        with open('static/data/category.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, operation_type_code, code = row
                operation_type = OperationType.objects.get(
                    code=operation_type_code,
                )
                Category.objects.get_or_create(
                    name=name,
                    operation_type=operation_type,
                    code=code,
                )
        self.stdout.write('Категории успешно импортированы.')

    def import_subcategories(self):
        with open('static/data/subcategory.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, category_code, code = row
                category = Category.objects.get(
                    code=category_code,
                )
                SubCategory.objects.get_or_create(
                    name=name,
                    category=category,
                    code=code,
                )
        self.stdout.write('Подкатегории успешно импортированы.')

    def handle(self, *args, **options):
        try:
            self.import_operation_types()
            self.import_operation_statuses()
            self.import_categories()
            self.import_subcategories()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Произошла ошибка при обработке файла: '
                    f'{str(e)}.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Данные успешно импортированы.')
            )
