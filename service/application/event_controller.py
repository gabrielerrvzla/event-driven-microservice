import json

from easy_log import EasyLog

from ..constants import ERROR_PARSE_MESSAGE
from ..infrastructure.kafka import KafkaConsumer, KafkaProducer
from ..settings import Settings


class EventController:
    def __init__(self, logger: EasyLog, settings: Settings):
        self.logger = logger
        self.settings = settings

        # Initialize producer
        self.producer = KafkaProducer(
            self.settings.KAFKA_SERVER,
            logger,
        )

        # Initialize consumer
        self.consumer = KafkaConsumer(
            self.settings.KAFKA_SERVER,
            self.settings.KAFKA_TOPICS,
            self.settings.KAFKA_GROUP_ID,
            self._handle_message,
            self._handle_error,
            logger,
        )

    def start(self):
        self.logger.info("Starting consuming messages")
        self.consumer.consume_messages()

    def _handle_message(self, message):
        data = message.value().decode("utf-8")
        data = json.loads(data)

        self.logger.info(f"Mensaje recibido: {data}")

    def _handle_error(self, error: Exception):
        # JSON parse error
        if isinstance(error, json.JSONDecodeError):
            self.logger.error(
                f"Error al parsear el mensaje: {error}",
                code=ERROR_PARSE_MESSAGE,
            )
