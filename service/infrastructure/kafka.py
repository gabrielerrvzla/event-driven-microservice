import time

from confluent_kafka import Consumer, KafkaError, Producer
from easy_log import EasyLog

from ..constants import ERROR_KAFKA_PRODUCER_SEND_MESSAGE


class KafkaConsumer:
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        message_handler: callable,
        error_handler: callable,
        logger: EasyLog,
        auto_offset_reset="earliest",
    ):
        """
        Inicializa el Kafka Consumer.
        - message_handler: función de callback para procesar los mensajes.
        - error_handler: función de callback para manejar errores.
        """
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = bootstrap_servers
        self.message_handler = message_handler
        self.error_handler = error_handler
        self.logger = logger

        # Configuración del consumidor
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "group.id": self.group_id,
                "auto.offset.reset": auto_offset_reset,
                "enable.auto.commit": False,
            }
        )

        # Suscripción al tópico
        self.consumer.subscribe([self.topic])

    def consume_messages(self, timeout: float = 1.0):
        """
        Método principal para consumir mensajes de Kafka con manejo de errores y confirmación manual.
        """
        try:
            while True:
                msg = self.consumer.poll(timeout)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # Fin de la partición alcanzada
                        self.logger.info(
                            f"Fin de la partición {msg.partition()} en {msg.topic()}"
                        )
                    else:
                        self.error_handler(msg.error())
                    continue

                try:
                    self.message_handler(msg)
                    self.consumer.commit(msg)
                except Exception as e:
                    self.error_handler(e)

        except KeyboardInterrupt:
            self.logger.info("El consumo fue interrumpido.")

        finally:
            self.consumer.close()

    def stop(self):
        """Método para detener el consumidor manualmente."""
        self.logger.info("Deteniendo el consumidor...")
        self.consumer.close()


class KafkaProducer:
    def __init__(
        self,
        bootstrap_servers: str,
        logger: EasyLog,
        max_retries=3,
        retry_delay=5,
    ):
        """
        Inicializa el Kafka Producer.
        - max_retries: número máximo de reintentos en caso de fallo al enviar el mensaje.
        - retry_delay: tiempo de espera en segundos entre reintentos.
        """

        self.bootstrap_servers = bootstrap_servers
        self.logger = logger
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Configuración del producer
        self.producer = Producer({"bootstrap.servers": self.bootstrap_servers})

    def produce_message(self, topic: str, message: str):
        """
        Produce un mensaje a Kafka y maneja las confirmaciones de envío y los errores.
        Si falla, intenta enviar el mensaje hasta `max_retries` veces con un retraso de `retry_delay` segundos.
        Si después de los reintentos falla, lanza un error crítico.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                # Intentar producir el mensaje
                self.producer.produce(topic, message.encode("utf-8"))
                self.producer.poll(0)  # Poll para enviar el mensaje de manera asíncrona
                self.logger.info(f"Mensaje enviado correctamente: {message} a {topic}")
                return
            except Exception as e:
                retries += 1
                self.logger.error(
                    f"Error al enviar el mensaje. Intento {retries} de {self.max_retries}: {e}",
                    code=ERROR_KAFKA_PRODUCER_SEND_MESSAGE,
                )
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error(
                        f"Error crítico: No se pudo enviar el mensaje '{message}' después de {self.max_retries} intentos.",
                        code=ERROR_KAFKA_PRODUCER_SEND_MESSAGE,
                    )

    def flush(self):
        """
        Forzar que todos los mensajes pendientes sean enviados.
        """
        self.producer.flush()

    def stop(self):
        """Detener el producer manualmente."""
        self.logger.info("Deteniendo el producer...")
        self.producer.flush()
