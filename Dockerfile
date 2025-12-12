# Imagen base
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos solo dependencias primero (mejor cache en builds)
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación
COPY . .

# Puerto que expone Uvicorn por defecto
EXPOSE 8000

# Comando para arrancar la app con Uvicorn
# Ajusta "app.main:app" según tu estructura (módulo:instancia)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
