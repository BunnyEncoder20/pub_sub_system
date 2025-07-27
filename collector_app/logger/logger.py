import logging
import sys
import structlog

from app_config import settings

def setup_logging():
    ''' Configure Basic logging for root logger in collector app '''

    logging.basicConfig(
        format = '%(message)s',
        stream = sys.stdout,
        level= settings.app.LOG_LEVEL
    )

    # StructLog config
    structlog.configure(
        processors = [
            structlog.contextvars.merge_contextvars,     #  For future context-based logging
            structlog.processors.TimeStamper(fmt="iso"), # Add timestamp
            structlog.processors.add_log_level,          # Add level (info, debug, etc.)
            structlog.dev.ConsoleRenderer()              # Pretty logs for dev
            # structlog.processors.JSONRenderer()        # For production logging in JSON format (optional)
        ],
        context_class=dict,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name: str = 'Collector_App'):
    return structlog.get_logger(name)
