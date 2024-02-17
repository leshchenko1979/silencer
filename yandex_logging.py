import logging
from pythonjsonlogger import jsonlogger


def init_logging(name: str = None, level=logging.INFO):
    logger = logging.getLogger(name)
    logging.getLogger().setLevel(level)
    root_handler = logging.getLogger().handlers[0]
    root_handler.setFormatter(YandexFormatter())
    logger.debug("Starting the main module")
    return logger


class YandexFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["logger"] = record.name
        log_record["level"] = record.levelname.replace("WARNING", "WARN").replace(
            "CRITICAL", "FATAL"
        )

    def format(self, record):
        return super().format(record).replace("\n", "\r")


logger = init_logging(__name__)
