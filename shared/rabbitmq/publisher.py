import json
import logging
import pika
from typing import Dict, Any
from connection import get_rabbitmq_connection

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    """
    A reusable RabbitMQ publisher class for publishing messages to queues and exchanges.
    """

    def __init__(self, rabbitmq_url: str):
        """
        Initialize the RabbitMQ publisher.

        Args:
            rabbitmq_url: RabbitMQ connection URL
        """
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    def connect(self) -> bool:
        """
        Establish connection to RabbitMQ.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = get_rabbitmq_connection(self.rabbitmq_url)
            if self.connection:
                self.channel = self.connection.channel()
                logger.info("RabbitMQ publisher connected successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to connect RabbitMQ publisher: {e}")
            return False

    def disconnect(self):
        """Close the RabbitMQ connection."""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("RabbitMQ publisher disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting RabbitMQ publisher: {e}")

    def declare_queue(self, queue_name: str, durable: bool = True) -> bool:
        """
        Declare a queue.

        Args:
            queue_name: Name of the queue to declare
            durable: Whether the queue should survive broker restarts

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.channel:
                logger.error("No active channel. Call connect() first.")
                return False

            self.channel.queue_declare(queue=queue_name, durable=durable)
            logger.info(f"Queue '{queue_name}' declared successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to declare queue '{queue_name}': {e}")
            return False

    def declare_exchange(self, exchange_name: str, exchange_type: str = 'direct', durable: bool = True) -> bool:
        """
        Declare an exchange.

        Args:
            exchange_name: Name of the exchange to declare
            exchange_type: Type of exchange (direct, topic, fanout, headers)
            durable: Whether the exchange should survive broker restarts

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.channel:
                logger.error("No active channel. Call connect() first.")
                return False

            self.channel.exchange_declare(
                exchange=exchange_name,
                exchange_type=exchange_type,
                durable=durable
            )
            logger.info(f"Exchange '{exchange_name}' declared successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to declare exchange '{exchange_name}': {e}")
            return False

    def publish_to_queue(
        self,
        queue_name: str,
        message: Dict[str, Any],
        declare_queue: bool = True,
        durable: bool = True
    ) -> bool:
        """
        Publish a message directly to a queue.

        Args:
            queue_name: Name of the queue to publish to
            message: Message payload as dictionary
            declare_queue: Whether to declare the queue before publishing
            durable: Whether the queue should be durable (if declaring)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.channel:
                logger.error("No active channel. Call connect() first.")
                return False

            # Declare queue if requested
            if declare_queue:
                if not self.declare_queue(queue_name, durable):
                    return False

            # Publish message
            message_body = json.dumps(message)
            properties = pika.BasicProperties(
                delivery_mode=2 if durable else 1,  # Make message persistent if durable
                content_type='application/json'
            )

            self.channel.basic_publish(
                exchange='',  # Default exchange
                routing_key=queue_name,
                body=message_body,
                properties=properties
            )

            logger.info(f"Message published to queue '{queue_name}': {message}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish message to queue '{queue_name}': {e}")
            return False

    def publish_to_exchange(
        self,
        exchange_name: str,
        routing_key: str,
        message: Dict[str, Any],
        exchange_type: str = 'direct',
        declare_exchange: bool = True,
        durable: bool = True
    ) -> bool:
        """
        Publish a message to an exchange with a routing key.

        Args:
            exchange_name: Name of the exchange to publish to
            routing_key: Routing key for the message
            message: Message payload as dictionary
            exchange_type: Type of exchange (if declaring)
            declare_exchange: Whether to declare the exchange before publishing
            durable: Whether the exchange should be durable (if declaring)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.channel:
                logger.error("No active channel. Call connect() first.")
                return False

            # Declare exchange if requested
            if declare_exchange:
                if not self.declare_exchange(exchange_name, exchange_type, durable):
                    return False

            # Publish message
            message_body = json.dumps(message)
            properties = pika.BasicProperties(
                delivery_mode=2 if durable else 1,  # Make message persistent if durable
                content_type='application/json'
            )

            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message_body,
                properties=properties
            )

            logger.info(f"Message published to exchange '{exchange_name}' with routing key '{routing_key}': {message}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish message to exchange '{exchange_name}': {e}")
            return False

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
