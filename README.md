# Proyecto de Transcripción Médica

Este proyecto permite la transcripción de audios enviados por WhatsApp a texto y guarda los informes en el sistema de archivos.

## Requisitos

- Python 3.9
- Google Cloud SDK configurado con acceso a Speech-to-Text API
- Twilio Account SID y Auth Token
- Docker

## Instalación

1. Clona este repositorio.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Configura las variables de entorno creando un archivo `.env` en la raíz del proyecto con el siguiente contenido:


4. Ejecuta la aplicación con `python app/main.py`.

## Uso

- Envía audios a través de WhatsApp al número configurado en Twilio.
- Usa la interfaz gráfica para seleccionar y transcribir audios localmente.

## Despliegue con Docker

1. Construye la imagen de Docker:

```sh
docker build -t medical-reporting .

2. Ejecuta el contenedor:

docker run -p 5000:5000 medical-reporting



### Resumen

Con estas actualizaciones, tu proyecto ahora tiene un archivo `.env` para manejar las variables de entorno, y el `Dockerfile` se ha ajustado para incluir este archivo en el contenedor. Además, el código se ha modificado para cargar estas variables de entorno usando `python-dotenv`. Esto asegura que tus claves de API y otros valores sensibles estén bien gestionados y protegidos.
