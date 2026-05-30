# Validation Service

Сервис асинхронной обработки и проверки заявок на доступ.
Работает как Kafka consumer и выполняет бизнес-валидацию перед выдачей прав.

## Стек

* Python asyncio
* aiokafka
* httpx
* Pydantic
* Docker

## Зона ответственности

Сервис отвечает за:

* получение событий из Kafka
* проверку конфликтующих групп прав
* валидацию заявок
* обновление статуса заявки
* инициирование выдачи или отклонения доступа

## Validation Rules

Система поддерживает конфликтующие группы прав.

Например:

* Developer
* Owner

Пользователь не может одновременно обладать конфликтующими группами.

Проверка выполняется до выдачи доступа.

## Процесс обработки

```text
Kafka Event
↓
AccessRequestHandler
↓
ValidationService
↓
Conflict Validation
↓
Grant / Reject
↓
Update Status
```

## Architecture

Сервис использует **Clean Architecture** и event-driven подход.

```text
application/
domain/
infrastructure/
```

Основные компоненты:

* KafkaConsumerClient
* AccessRequestHandler
* ValidationService

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
3) Из той же директории запускаем приложение:
```bash
python -m app.main
```
