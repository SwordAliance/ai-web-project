
Учебный AI-веб-сервис с асинхронной обработкой задач, REST API, WebSocket, PostgreSQL, Redis, Celery, миграциями Alembic, reverse proxy на Nginx и мониторингом через Prometheus + Grafana.

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

## Структура проекта


ai_web_project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tasks/
│   │   └── main.py
│   ├── alembic/
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
├── ui/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── infra/
│   ├── prometheus/
│   └── grafana/
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
└── README.md
