from __future__ import annotations

import os
import time

import pandas as pd
import requests
import streamlit as st

API_INTERNAL_URL = os.getenv("API_INTERNAL_URL", "http://api:8000")
TIMEOUT = 15

st.set_page_config(page_title="AI Web Service", page_icon="🤖", layout="wide")
st.title("AI Web Service")
st.caption("UI общается только с API по REST и WebSocket через Nginx.")

session = requests.Session()


def api_get(path: str):
    response = session.get(f"{API_INTERNAL_URL}{path}", timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict):
    response = session.post(f"{API_INTERNAL_URL}{path}", json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


left, right = st.columns([2, 1])

with left:
    prompt = st.text_area(
        "Prompt",
        value="Сделай краткое описание архитектуры сервиса",
        height=150,
    )
    creativity = st.slider("Creativity", 0.0, 1.0, 0.4, 0.05)

    start = st.button("Отправить", type="primary")

    if start:
        try:
            with st.spinner("Запрос отправлен в очередь. Ждём результат по WebSocket..."):
                created = api_post("/api/predict", {"prompt": prompt, "creativity": creativity})
                task_id = created["task_id"]

                st.info(f"Task ID: {task_id}")

                ws_html = f"""
                <div id="status">Ожидание результата...</div>
                <pre id="output"></pre>
                <script>
                    const statusBox = document.getElementById("status");
                    const outputBox = document.getElementById("output");
                    const ws = new WebSocket("ws://" + window.location.host + "/api/ws/{task_id}");
                    ws.onopen = () => {{
                        statusBox.innerText = "WebSocket подключен. Ждём обновление...";
                        ws.send("ping");
                    }};
                    ws.onmessage = (event) => {{
                        const data = JSON.parse(event.data);
                        statusBox.innerText = "Статус: " + data.status;
                        outputBox.innerText = JSON.stringify(data, null, 2);
                        if (data.status === "success" || data.status === "failed") {{
                            ws.close();
                        }}
                    }};
                    ws.onerror = () => {{
                        statusBox.innerText = "Ошибка WebSocket";
                    }};
                </script>
                """
                st.components.v1.html(ws_html, height=260)

                # fallback: проверка статуса, если пользователь не держит страницу открытой
                for _ in range(10):
                    time.sleep(0.5)
                    try:
                        status = api_get(f"/api/tasks/{task_id}")
                    except requests.RequestException:
                        continue
                    if status["status"] in {"success", "failed"}:
                        st.success("Задача завершена")
                        if status["status"] == "success" and status.get("result"):
                            st.write(status["result"])
                        elif status.get("error"):
                            st.error(status["error"])
                        break

        except requests.RequestException:
            st.error("Сервис временно недоступен")

with right:
    st.subheader("Health")
    try:
        health = api_get("/api/health")
        st.json(health)
    except requests.RequestException:
        st.error("Backend недоступен")

    st.subheader("История")
    try:
        history = api_get("/api/history?limit=5")
        df = pd.DataFrame(history["items"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    except requests.RequestException:
        st.info("История пока недоступна")

st.divider()
st.write("Доступные страницы: /api/docs, /api/health, /api/metrics, Prometheus, Grafana.")
