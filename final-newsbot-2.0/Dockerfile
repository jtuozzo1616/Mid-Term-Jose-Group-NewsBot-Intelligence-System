FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements-app.txt requirements-core.txt ./
RUN pip install --no-cache-dir -r requirements-app.txt
COPY newsbot2/ ./newsbot2/
COPY data/ ./data/
EXPOSE 8000
CMD ["uvicorn","newsbot2.api:app","--host","0.0.0.0","--port","8000"]
