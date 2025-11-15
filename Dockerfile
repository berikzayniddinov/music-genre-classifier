# Используем Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем backend и frontend
COPY backend/app ./app
COPY backend/models ./backend/models
COPY frontend/templates ./frontend/templates
COPY frontend/static ./frontend/static

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Открываем порт
EXPOSE 8000

# Запуск сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
