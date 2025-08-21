FROM python:3.12-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia aplicação
COPY ./app ./app

# Executa a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
