FROM python:3.11-slim

WORKDIR /app

# Copiamos e instalamos las dependencias primero (aprovecha la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiamos todo el resto del código del proyecto a la carpeta de trabajo
COPY . .

EXPOSE 8000

# Como main.py está en la raíz, lo llamamos directo como main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]