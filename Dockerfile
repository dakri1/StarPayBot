# Используем официальный образ Python в качестве базового
FROM python:3.10-slim

# Установим рабочую директорию
WORKDIR /app

COPY requirements.txt ./
COPY main.py ./
COPY database ./database/

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Укажем, что контейнер слушает на порту 5000
EXPOSE 5000

# Команда, которая будет выполняться при запуске контейнера
CMD ["bash", "-c", "python database/migrations.py && python main.py"]
