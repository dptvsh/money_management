# Тестовое задание Первая IT-компания на позицию Python разработчика

Необходимо было реализовать веб-сервис для управления движением денежных средств (ДДС).

## Стек технологий

- Django
- Django Rest Framework
- PostgreSQL/SQLite
- Docker

## Реализованные функции

### Основные функции

- Создание записи о ДДС с полями:

  - Дата (автозаполнение с возможностью редактирования)

  - Статус (Бизнес/Личное/Налог + возможность расширения)

  - Тип (Пополнение/Списание + возможность расширения)

  - Категория и подкатегория (с возможностью расширения)

  - Сумма (в рублях)

  - Комментарий (необязательное поле)

- Просмотр списка записей с:

  - Табличным представлением данных

  - Фильтрацией по дате, статусу, типу, категории и подкатегории

  - Редактирование и удаление существующих записей

### Управление справочниками

- Добавление/редактирование/удаление:

  - Статусов

  - Типов операций

  - Категорий и подкатегорий

- Установление связей:

  - Подкатегории привязаны к категориям

  - Категории привязаны к типам операций

### Логические зависимости

- Можно выбрать только ту категорию, которая относится к выбранному типу, иначе возникнет ошибка

- Можно выбрать только ту подкатегорию, которая относится к выбанной категории, иначе возникнет ошибка

### Валидация

- Обязательные поля: сумма, тип, категория, подкатегория

- Валидация на стороне клиента и сервера

## Что можно улучшить:

- Добавить модель пользователя для разграничения прав доступа; возможно добавить админа, который и будет отвечать за редактирование справочной информации.
- Добавить более удобный интерфейс.
- Добавить теги для более гибкой категоризации.

## Как развернуть проект локально с помощью Docker

1. Клонировать репозиторий и перейти в него в командной строке:

   ```git clone https://github.com/dptvsh/money_management.git```

   ```cd money_management```

2. Создать и заполнить .env файл по образцу из .env.example. Созданный файл .env должен находиться в той же директории, что и образец.

3. Запустить контейнеры в фоновом режиме:
  
   ```docker compose up -d```

4. Последовательно собрать и скопировать статику:

   ```docker compose exec backend python manage.py collectstatic```

   ```docker compose exec backend cp -r /app/collected_static/. /backend_static/static/```

5. Применить миграции:

   ```docker compose exec backend python manage.py migrate```

6. Создать суперпользователя:

   ```docker compose exec backend python manage.py createsuperuser```

7. Заполнить базу данных начальными значениями (типы и статусы операций, категории и подкатегории):
  
   ```docker compose exec backend python manage.py load_data```

## Примеры API запросов и ответов

В проекте доступны следующие эндпоинты:

- Админка: http://localhost:8000/admin/
- Общий API: http://localhost:8000/api/
- Записи: http://localhost:8000/api/records/
- Типы операций: http://localhost:8000/api/operation_types/
- Статусы операций: http://localhost:8000/api/operation_statuses/
- Категории: http://localhost:8000/api/categories/
- Подкатегории: http://localhost:8000/api/subcategories/

### Основные функции

**Получение информации о всех записях:**

- Запрос:
  ```GET /api/records/```

- Пример ответа:
  ```json
  [
    {
        "created_at": "2025-07-31T14:08:24.968719Z",
        "operation_date": "30.07.2025",
        "status": "business",
        "operation_type": "income",
        "category": "infrastructure_income",
        "subcategory": "vps_income",
        "amount": "123.00",
        "comment": ""
    },
    {
        "created_at": "2025-07-31T14:13:33.116264Z",
        "operation_date": "29.07.2025",
        "status": "tax",
        "operation_type": "expense",
        "category": "marketing_expense",
        "subcategory": "avito_expense",
        "amount": "365.00",
        "comment": "Комментарий для пробы"
    }
  ]
  ```

**Внесение новой записи:**

- Запрос: `POST /api/records/`

- Пример запроса:
  ``` json
    {
        "operation_date": "30.07.2025",
        "status": "business",
        "operation_type": "income",
        "category": "infrastructure_income",
        "subcategory": "vps_income",
        "amount": "123"
    }
  ```
- Пример ответа:
  ``` json
    {
        "created_at": "2025-07-31T14:08:24.968719Z",
        "operation_date": "30.07.2025",
        "status": "business",
        "operation_type": "income",
        "category": "infrastructure_income",
        "subcategory": "vps_income",
        "amount": "123.00",
        "comment": ""
    }
  ```

### Управление справочниками

**Получение всех категорий:**

- Запрос: `GET /api/categories/`

- Пример ответа:
  ```json
  [
    {
        "name": "Инфраструктура",
        "operation_type": "expense",
        "code": "infrastructure_expense"
    },
    {
        "name": "Инфраструктура",
        "operation_type": "income",
        "code": "infrastructure_income"
    },
    {
        "name": "Маркетинг",
        "operation_type": "expense",
        "code": "marketing_expense"
    },
    {
        "name": "Маркетинг",
        "operation_type": "income",
        "code": "marketing_income"
    }
  ]
  ```

**Получение одной категории (используется slug):**

- Запрос: `GET /api/categories/marketing_income/`

- Пример ответа:
  ```json
   {
        "name": "Маркетинг",
        "operation_type": "income",
        "code": "marketing_income"
    }
  ```

**Создание новой категории:**

- `POST /api/categories/`

- Пример запроса:

  ```json
  {
      "name": "Жизнь",
      "operation_type": "expense",
      "code": "life"
  }
  ```

- Пример ответа:

  ```json
  {
      "name": "Жизнь",
      "operation_type": "expense",
      "code": "life"
  }
  ```