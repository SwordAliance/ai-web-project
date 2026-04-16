# AI Web Project

Учебный AI-веб-сервис, который показывает полный цикл инженерного проекта:

- FastAPI backend
- Celery + Redis для асинхронных задач
- PostgreSQL + SQLAlchemy + Alembic
- Streamlit UI
- Nginx reverse proxy
- Prometheus + Grafana
- WebSocket для получения результата без polling

## Запуск

```bash
cp .env.example .env
docker compose up --build -d
```

## Архитектура

Пользователь -> Nginx -> UI / API  
UI -> REST API для запуска задачи  
UI <-...-> WebSocket <-...-> API для получения результата  
API -> Celery -> Worker -> ML service  
API -> PostgreSQL  
API/Worker -> Redis  
Prometheus -> API `/metrics`  
Grafana -> Prometheus

## Основные эндпоинты

- `GET /v1/health`
- `POST /v1/predict`
- `GET /v1/tasks/{task_id}`
- `GET /v1/history`
- `WS /v1/ws/{task_id}`
- `GET /metrics`

## Что закрыто по критериям

- lifespan для инициализации Redis, БД и модели
- Celery + Redis
- строгая Pydantic-валидация
- кастомные обработчики ошибок
- отдельный ML-сервис
- логирование всех этапов
- ORM и Alembic миграции
- health checks
- Prometheus и Grafana
- Nginx reverse proxy и rate limiting
- Docker Compose с сетями, volumes и порядком запуска
- WebSocket вместо polling в UI

## Примечания по запуску

В проекте есть сервис `migrate`, который перед стартом API и worker выполняет:

```bash
alembic upgrade head
```

Это делает запуск воспроизводимым одной командой `docker compose up --build -d`.
