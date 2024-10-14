from easy_log import EasyLog

from .application.event_controller import EventController
from .settings import Settings


def main():
    settings = Settings()
    logger = EasyLog(settings.NAME, settings.LOG_LEVEL)
    controller = EventController(logger, settings)
    controller.start()


if __name__ == "__main__":
    main()
