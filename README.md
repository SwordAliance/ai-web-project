AI-веб-сервис с асинхронной обработкой задач, REST API, WebSocket, PostgreSQL, Redis, Celery, миграциями Alembic, reverse proxy на Nginx и мониторингом через Prometheus + Grafana.

## Возможности

- REST API на FastAPI
- Асинхронная обработка задач через Celery
- Redis как брокер и backend результатов
- WebSocket для получения результата без polling
- PostgreSQL для хранения истории запросов
- SQLAlchemy ORM и Alembic миграции
- Streamlit UI
- Nginx как единая точка входа
- Health checks для критичных сервисов
- Метрики для Prometheus и дашборд в Grafana

## Архитектура

Пользователь -> Nginx -> UI / API  
API -> Redis -> Celery Worker -> ML Service  
API -> PostgreSQL  
API -> Prometheus -> Grafana

## Логика работы
- Пользователь отправляет запрос через UI.
- UI вызывает backend API.
- API создаёт Celery-задачу.
- Worker обрабатывает задачу.
- Результат передаётся клиенту через WebSocket.
- История запросов сохраняется в PostgreSQL.
- Метрики доступны в Prometheus и Grafana.

# Основные решения
- Backend и worker разделены
- API stateless
- Состояние задач вынесено в Redis / PostgreSQL
- WebSocket используется вместо постоянного polling
- Nginx выступает единой точкой входа
- Все сервисы должны запускаться одной командой

# Запуск 
docker compose up --build -d
