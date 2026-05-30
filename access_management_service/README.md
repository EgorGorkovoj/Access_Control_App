# Access Management Service

Сервис управления доступами и основными доменными объектами системы контроля доступа.

## Стек сервиса

* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Alembic
* Pydantic V.2
* Docker

## Ответственность сервиса

Сервис отвечает за хранение и управление:

* ресурсами (**Resource**)
* доступами (**Access**)
* группами прав (**Right Group**)
* связями групп и доступов
* пользовательскими правами
* заявками на доступ

Также сервис предоставляет API для:

* выдачи прав пользователям
* отзыва прав
* получения effective permissions
* изменения статуса заявок
* различные служебные методы для CRUD операций

## Архитектура

Сервис построен по принципам **Clean Architecture**.

```text
application/
domain/
infrastructure/
presentation/
```

## Запуск локально
1) Создаем файл .env в корне сервиса. Пример содержимого файла находится в .env.example.
2) Создаем виртуальное окружение:
```bash
python -m venv venv
```
#### Активировать:
- Windows
```bash
source venv\Scripts\activate
```
- Linux / macOS
```bash
source venv/bin/activate
```
3) Поднимаем базу данных из директории access management service:
```bash
docker compose -f docker-compose.yml up -d
```
4) Из той же директории запускаем сервер:
```bash
uvicorn app.main:app --reload
```