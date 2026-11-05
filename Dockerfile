FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей, если понадобятся для сборки
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Копируем требования и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Команда для запуска приложения (миграции будут применяться перед стартом или внутри)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]