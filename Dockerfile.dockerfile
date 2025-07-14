# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:create_app()"]