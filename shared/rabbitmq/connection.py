import pika
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


def get_rabbitmq_connection(rabbitmq_url: str, max_retries: int = 5) -> Optional[pika.BlockingConnection]:
    """
    Create a RabbitMQ connection with retry logic.

    Args:
        rabbitmq_url: RabbitMQ connection URL
        max_retries: Maximum number of connection attempts

    Returns:
        pika.BlockingConnection or None if failed
    """
    for attempt in range(max_retries):
        try:
            parameters = pika.URLParameters(rabbitmq_url)       # parses url like 'amqp://guest:guest@localhost:5672/'
            connection = pika.BlockingConnection(parameters)    # BlockingConnection creates a direct connectoin to RabbitMQ
            logger.info("Successfully connected to RabbitMQ")
            return connection

        except Exception as e:
            wait_time = 2 ** attempt    # exponential backoff: 1s, 2s, 4s, 8s, 16s, 32s...
            logger.warning(
                f"Failed to connect to RabbitMQ | attempt {attempt + 1}/{max_retries}: {e}. "
                f"Retrying in {wait_time} seconds..."
            )
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                logger.error("Failed to connect to RabbitMQ after all attempts")
                return None
