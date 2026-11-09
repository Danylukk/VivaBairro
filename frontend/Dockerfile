FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/code
WORKDIR /code
COPY frontend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend /code/frontend
# A mesma configuracao de tema da execucao local deve valer no Docker.
COPY .streamlit /code/.streamlit
EXPOSE 8501
CMD ["streamlit", "run", "frontend/app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true", "--browser.gatherUsageStats", "false"]
