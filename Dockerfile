FROM python:3.13-slim

WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY reqs.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Сообщаем, какой порт будет использовать контейнер
EXPOSE 5000

# Команда для запуска приложения
# Важно: используем gunicorn для production, а не встроенный сервер Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]