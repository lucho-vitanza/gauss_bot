# Utiliza una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo de credenciales de Google Cloud
COPY path/to/your/google-cloud-credentials.json /app/google-cloud-credentials.json

# Establece la variable de entorno para las credenciales de Google Cloud
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/google-cloud-credentials.json"

# Copia el archivo .env
COPY .env .env

# Exponer el puerto para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app/main.py"]
