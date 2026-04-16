# AI Web Service

AI-веб-сервис с асинхронной обработкой запросов, WebSocket-уведомлениями, PostgreSQL, Celery, Redis, Nginx, Alembic, Prometheus и Grafana.

## Архитектура

Пользователь → Nginx → UI / API  
API → Redis (broker) → Celery Worker → ML Service  
API → PostgreSQL  
Prometheus → Grafana

## Возможности

- REST API на FastAPI
- Асинхронные задачи через Celery
- WebSocket для получения результата без polling
- ORM: SQLAlchemy
- Миграции: Alembic
- Health checks
- Метрики Prometheus
- Дашборд Grafana
- UI на Streamlit
- Reverse proxy на Nginx

## Запуск

```bash
cp .env.example .env
docker compose up --build -d
```

## Доступ

- UI: http://localhost
- API docs: http://localhost/api/docs
- Health: http://localhost/api/health
- Metrics: http://localhost/api/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Пример запроса

```bash
curl -X POST http://localhost/api/predict \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Привет", "creativity":0.5}'
```

## Структура

```text
backend/   API, worker, DB, services
ui/        Streamlit интерфейс
nginx/     reverse proxy
infra/     Prometheus и Grafana
```
