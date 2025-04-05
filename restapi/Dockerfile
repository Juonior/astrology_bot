FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости первыми для лучшего кэширования
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всю папку app целиком
COPY app ./app

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app

# Команда запуска
CMD ["python", "app/main.py"]