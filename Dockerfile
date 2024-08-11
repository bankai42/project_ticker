# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем зависимости для PostgreSQL
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Выполняем миграции
RUN python manage.py migrate

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
