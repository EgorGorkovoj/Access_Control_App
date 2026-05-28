# Access_Control_App

Система управления доступами на основе микросервисной архитектуры.

---

## 📌 Описание

Проект реализует систему контроля и выдачи доступов к ресурсам.
Система предназначена для:
- управления ресурсами;
- управления доступами;
- управления группами прав;
- выдачи и отзыва прав пользователям;
- обработки заявок на получение доступа;
- проверки конфликтующих групп прав.

---

## Архитектура

Система построена в виде набора микросервисов.

Сервисы:
- Access Management Service
- Access Validation Service
- Api Gateway Service

## 📦 Основной стек приложения

- Python 3.12
- PostgreSQL 17
- FastApi
- SQLAlchemy 2.0
- Pydantic V2
- Kafka
- Docker
- asyncio
- pip / venv

---

## Общая схема взаимодействия
```text
Client
↓
Api Gateway
↓
Создание заявки + Отправка события в Kafka
↓                          ↓
Access Management Service  Kafka
                           ↓
                           Validation Service (Проверка конфликтов)
                           ↓
                           Access Management Service
↓
Выдача прав
↓
Обновление статуса заявки
```
Подробная схема находится в директории docs корня проекта.
# 🚀 Установка и запуск

## 1. Создать виртуальное окружение

```bash
python -m venv venv
```

### Активировать:
- Windows
```bash
source venv\Scripts\activate
```
- Linux / macOS
```bash
source venv/bin/activate
```

## 2. Установка зависимостей
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# Поднятие всего приложения

## 1. Создать файл .env в корне проекта и во всех микросервисах.

Пример содержания файла .env находится в корне проекта в файле .env.example.

## 2. Из корневой директории проекта выполнить команду:
```bash
docker compose -f docker-compose.yml up -d
```

## 3. Миграции Alembic

В папке alembic/verisons/ сервиса Access Management Service должна лежать действующая миграция.
Если ее нет по какой-то причине, можно поднять отдельно БД через докер и выполнить команду в корневой директории сервиса:
```bash
alembic revision --autogenerate -m "Initial commit"
```
Миграции применяются автоматически.

# Логирование

Все события пишутся в:
```
logs/app.log
```
## 👨‍💻 Автор
[Егор Горьковой](https://github.com/EgorGorkovoj)