import logging.config
import sys
from pathlib import Path

from app.core.config import settings

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True, parents=True)

LOG_FILE = LOG_DIR / 'app.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': """
                asctime: %(asctime)s
                funcName: %(funcName)s
                levelname: %(levelname)s
                message: %(message)s
                process: %(process)d
                processName: %(processName)s
                thread: %(thread)d
                threadName: %(threadName)s
                exc_info: %(exc_info)s
            """,
        },
    },
    'handlers': {
        'console': {
            'level': settings.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
        'file': {
            'level': settings.LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_FILE),
            'maxBytes': 5_000_000,
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': settings.LOG_LEVEL,
            'propagate': True,
        },
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING)
