FROM python:3.14-slim

WORKDIR /m.tolstogyzowa_final_project

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "-n", "auto", "-v"]

