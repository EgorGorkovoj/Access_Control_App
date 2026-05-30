# API Gateway

Gateway предоставляет единую точку входа для клиентских запросов и маршрутизирует их во внутренние сервисы.

## Стек

* FastAPI
* httpx
* Kafka
* asyncio
* Docker

## Зона ответственности

Gateway отвечает за:

* маршрутизацию запросов
* proxy к внутренним сервисам
* изоляцию внутренних сервисов от клиента
* публикацию событий в Kafka

Gateway не содержит бизнес-логики.

## Kafka Integration

При создании заявки Gateway:

1. принимает запрос клиента
2. отправляет данные в Access Management Service
3. публикует событие в Kafka
4. инициирует процесс валидации

Gateway выступает **Kafka Producer** для Validation Service.

## Interaction Flow

```text
Client
↓
API Gateway
↓
Создание заявки
↓
Access Management Service
↓
Kafka Event
↓
Validation Service
↓
Проверка конфликтов
↓
Access Management Service
↓
Выдача прав / Обновление статуса
```

## Архитектура

Gateway сервис построен по принципам слоистой архитектуры, разделяя transport layer, service layer и integration layer.

Основные задачи:

- маршрутизация запросов
- перенаправление запросов во внутренние сервисы
- публикация событий в Kafka
- координация обработки запросов

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
3) Из той же директории запускаем сервер:
```bash
uvicorn app.main:app --reload
```
