# Usa una imagen base oficial de Python 3.10 (o la versión que estés usando)
FROM python:3.10-slim

# Actualizar el índice de paquetes de la imagen base e instalar git
RUN apt-get update && apt-get install -y git

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /core

# Copiar el archivo de requerimientos
COPY ./requirements.txt /service/requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r /service/requirements.txt

# Copiar el código de la aplicación dentro del contenedor
COPY ./service service
