# Сервис управления отпусками сотрудников

## Описание

Этот сервис предоставляет HTTP API для управления информацией об отпусках сотрудников.

Функциональные возможности:
1. **Добавление отпуска** – позволяет указать ID сотрудника и даты отпуска.
2. **Получение 3 последних отпусков сотрудника**.
3. **Получение всех отпусков за указанный период**.
4. **Удаление информации об отпуске**.

## Технологии
- **Язык**: Python
- **Веб-фреймворк**: FastAPI
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy
- **Миграции**: Alembic
- **Тестирование**: Pytest, HTTPX
- **Статическая проверка кода**: Flake8, Black

## Установка и запуск

Создайте `.env` файл в корне проекта с переменными окружения, например:

```bash
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=leave_db
POSTGRES_PORT=5435
```

Затем выполните команду для сборки и запуска контейнеров:

```bash
docker-compose up --build -d
```
Установите зависимости:
```bash
pip install -r requirements.txt
```
Запустите миграции базы данных. Если файла alembic.ini ещё нет, нужно запустить в терминале команду:
```bash
alembic init migrations
```
После этого будет создана папка с миграциями и конфигурационный файл для алембика.

- В alembic.ini нужно задать адрес базы данных для миграций изменив sqlalchemy.url. Например:
```bash
sqlalchemy.url = postgresql://user:password1234@127.0.0.1:5435/leave_db
```
- Дальше в папке с миграциями и открыть env.py, там вносим следующие изменения:

```bash
from db.models import Base
# from myapp import mymodel
target_metadata = Base.metadata
#target_metadata = None
```
Создаем миграции:
```bash
alembic revision --autogenerate -m "comment"
```
Дальше вводим:
```bash
alembic upgrade heads
```

## Тестирование

Запускаем тесты.
При первом запуске тесты упадут! После падения в папке tests создадутся алембиковские файлы, туда нужно прописать данные
по миграциям аналогично пунктам выше. Путь соответственно должен быть уже к тестовой базе.
- В alembic.ini нужно задать адрес тестовой базы данных для миграций изменив sqlalchemy.url. Например:
```bash
sqlalchemy.url = postgresql://postgres_test:postgres_test@127.0.0.1:5436/postgres_test
```
- Дальше в папке с миграциями и открыть env.py, там вносим следующие изменения:

```bash
from db.models import Base
# from myapp import mymodel
target_metadata = Base.metadata
#target_metadata = None
```
После этого можно повторно запускать тесты.

## API Методы

### Добавление отпуска
**POST** `/leaves/`
#### Тело запроса (JSON):
```json
{
  "employee_id": 1,
  "start_date": "2025-06-01",
  "end_date": "2025-06-15"
}
```
#### Ответ (успешно):
```json
{
  "employee_id": 1,
  "start_date": "2025-06-01",
  "end_date": "2025-06-15",
  "id": 0
}
```

### Получение 3 последних отпусков сотрудника
**GET** `/leaves/{employee_id}/recent`
#### Пример ответа:
```json
[
  { "employee_id": 1, "start_date": "2025-04-10", "end_date": "2025-04-20", "id": 2 },
  { "employee_id": 1, "start_date": "2025-02-15", "end_date": "2025-02-25", "id": 1 }
]
```

### Получение всех отпусков за период
**GET** `/leaves/?start_date=2025-01-01&end_date=2025-12-31`
#### Пример ответа:
```json
[
  { "employee_id": 2, "start_date": "2025-05-10", "end_date": "2025-05-20", "id": 1 }
]
```

### Удаление отпуска
**DELETE** `/leaves/{leave_id}`
#### Пример ответа (успешно):
```json
{
  "detail": "Отпуск удален"
}
```
