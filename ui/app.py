from __future__ import annotations

import json
import os
from typing import Any

import pandas as pd
import requests
import streamlit as st
from websocket import WebSocketTimeoutException, create_connection

API_INTERNAL_URL = os.getenv("API_INTERNAL_URL", "http://api:8000/v1")
UI_PORT = int(os.getenv("UI_PORT", "8501"))
TIMEOUT = 10


st.set_page_config(page_title="AI Web Project", page_icon="🤖", layout="wide")
st.title("AI Web Project")
st.caption("UI общается с backend через REST для запуска задачи и через WebSocket для получения результата.")

session = requests.Session()


def api_get(path: str) -> dict[str, Any]:
    response = session.get(f"{API_INTERNAL_URL}{path}", timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = session.post(f"{API_INTERNAL_URL}{path}", json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def ws_url(task_id: str) -> str:
    base = API_INTERNAL_URL.replace("http://", "ws://").replace("https://", "wss://")
    return f"{base}/ws/{task_id}"


def safe_request(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs), None
    except requests.RequestException:
        return None, "Сервис временно недоступен"


left, right = st.columns([2, 1])

with left:
    prompt = st.text_area(
        "Запрос",
        value="Объясни, зачем нужен Celery в этом проекте",
        height=140,
    )
    creativity = st.slider("Creativity", 0.0, 1.0, 0.35, 0.05)

    submitted = st.button("Отправить", type="primary")

    if submitted:
        try:
            with st.spinner("Создаю задачу и ожидаю результат по WebSocket..."):
                created = api_post("/predict", {"prompt": prompt, "creativity": creativity})
                task_id = created["task_id"]

                st.info(f"Task ID: {task_id}")
                placeholder = st.empty()

                ws = create_connection(ws_url(task_id), timeout=TIMEOUT)
                ws.settimeout(1.0)

                result = None
                try:
                    for _ in range(60):
                        try:
                            raw = ws.recv()
                            result = json.loads(raw)
                            break
                        except WebSocketTimeoutException:
                            placeholder.write("Ожидаю сообщение по WebSocket...")
                finally:
                    ws.close()

                if result is None:
                    st.warning("Результат ещё не готов")
                elif result.get("status") == "failed":
                    st.error(result.get("error") or "Ошибка выполнения")
                else:
                    st.success("Результат получен")
                    st.subheader("Ответ")
                    st.write(result["answer"])

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Intent", result.get("intent") or "—")
                    c2.metric(
                        "Confidence",
                        f"{result.get('confidence'):.3f}" if result.get("confidence") is not None else "—",
                    )
                    c3.metric("Status", result.get("status", "—"))

                    alts = result.get("alternatives") or []
                    if alts:
                        st.subheader("Альтернативы")
                        df = pd.DataFrame(alts)
                        st.bar_chart(df.set_index("intent"))
        except requests.RequestException:
            st.error("Сервис временно недоступен")
        except Exception:
            st.error("Не удалось получить ответ по WebSocket")

with right:
    st.subheader("Health")
    health, err = safe_request(api_get, "/health")
    if err:
        st.error(err)
    elif health:
        st.json(health)

    st.subheader("История")
    history, err = safe_request(api_get, "/history?limit=5")
    if err:
        st.info("История недоступна")
    elif history:
        st.dataframe(pd.DataFrame(history["items"]), use_container_width=True, hide_index=True)

    st.subheader("Метрики")
    st.caption("Метрики доступны через Prometheus и Grafana.")

st.divider()
st.markdown("### Примеры API")
st.code(
    """curl -X POST http://localhost/api/v1/predict \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Привет","creativity":0.5}'""",
    language="bash",
)
