# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /sistema-asistencia-backend

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar solo el código del backend
COPY *.py .
COPY database.py .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar (PRODUCCIÓN con uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]