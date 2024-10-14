# **Event-Driven Microservice Template**

Este proyecto es una base para la creación de microservicios orientados a eventos, que utiliza **Kafka** como sistema de mensajería, **Celery** para tareas distribuidas, y **Minio** (opcional) para almacenamiento de objetos. El servicio se gestiona con **Docker** y **Docker Compose**, facilitando el despliegue y la configuración.

## **Requisitos**

Asegúrate de tener instalados los siguientes programas en tu sistema:

- **Docker**: [Guía de instalación](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Guía de instalación](https://docs.docker.com/compose/install/)

## **Instrucciones de Uso**

### **1. Clonar el repositorio**

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/gabrielerrvzla/event-driven-microservice.git
cd event-driven-microservice
```

### **2. Configuración de variables de entorno**

Debes definir las siguientes variables de entorno en un archivo `.env`. Puedes copiar el archivo de ejemplo y modificarlo según tus necesidades:

```bash
cp .env.example .env
```

Edita el archivo `.env` y agrega las variables necesarias:

```bash
NAME="event-driven-microservice"
DEBUG="True"
LOG_LEVEL="DEBUG"

KAFKA_SERVER=localhost:9092
KAFKA_GROUP_ID=event-driven-group
KAFKA_TOPICS=events-topic

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

MINIO_HOST=localhost:9000
MINIO_ACCESS_KEY=your-minio-access-key
MINIO_SECRET_KEY=your-minio-secret-key
MINIO_BUCKET_NAME=your-bucket
MINIO_SECURE=False
```

### **Variables de entorno**

| Variable                | Descripción                                        | Obligatoria | Valor por defecto           |
| ----------------------- | -------------------------------------------------- | ----------- | --------------------------- |
| `NAME`                  | Nombre del microservicio                           | Sí          | `event-driven-microservice` |
| `DEBUG`                 | Modo de depuración (`True` o `False`)              | Sí          | `True`                      |
| `LOG_LEVEL`             | Nivel de logueo (`DEBUG`, `INFO`, `ERROR`)         | Sí          | `DEBUG`                     |
| `KAFKA_SERVER`          | Dirección del servidor Kafka                       | Sí          |                             |
| `KAFKA_GROUP_ID`        | ID del grupo de consumidores de Kafka              | Sí          |                             |
| `KAFKA_TOPICS`          | Lista de tópicos de Kafka separados por comas      | Sí          |                             |
| `CELERY_BROKER_URL`     | URL del broker para Celery                         | Sí          |                             |
| `CELERY_RESULT_BACKEND` | Backend para almacenar los resultados de Celery    | Sí          |                             |
| `MINIO_HOST`            | Dirección del servidor Minio                       | No          |                             |
| `MINIO_ACCESS_KEY`      | Clave de acceso de Minio                           | No          |                             |
| `MINIO_SECRET_KEY`      | Clave secreta de Minio                             | No          |                             |
| `MINIO_BUCKET_NAME`     | Nombre del bucket de Minio                         | No          |                             |
| `MINIO_SECURE`          | Indica si se usa HTTPS en Minio (`True` o `False`) | No          | `False`                     |

> Nota: Las variables de Minio son opcionales, ya que no todos los microservicios pueden necesitar almacenamiento de objetos.

### **3. Construcción y ejecución del proyecto**

Para construir y ejecutar los servicios, simplemente ejecuta:

```bash
docker-compose up --build
```

Esto levantará los contenedores definidos en `docker-compose.yml`, que incluyen Kafka, Celery, Redis, y Minio (si está configurado).

### **4. Monitoreo de los logs**

Puedes monitorear los logs de los contenedores con:

```bash
docker-compose logs -f
```

Esto te permitirá ver los logs en tiempo real.

### **5. Detener los servicios**

Para detener todos los servicios, ejecuta:

```bash
docker-compose down
```

Esto detendrá y eliminará los contenedores asociados a tu servicio.

## **Servicios incluidos**

1. **Kafka**: Sistema de mensajería basado en eventos.
2. **Celery**: Sistema de colas distribuidas para ejecutar tareas asíncronas.
3. **Minio** (opcional): Almacenamiento de objetos similar a S3, si tu servicio requiere manejo de archivos.
4. **Logger**: Sistema de logs basado en la configuración del nivel de logueo (`DEBUG`, `INFO`, `ERROR`).


## **Contribuciones**

Si deseas contribuir a este proyecto, sigue los siguientes pasos:

1. Crea un **fork** del repositorio.
2. Crea una rama con tus cambios: `git checkout -b mi-rama`.
3. Haz un **commit** de tus cambios: `git commit -m 'Agregué una nueva característica'`.
4. Haz un **push** a la rama: `git push origin mi-rama`.
5. Abre un **Pull Request** en GitHub.

## **Licencia**

Este proyecto está bajo la licencia [MIT License](https://opensource.org/licenses/MIT).
