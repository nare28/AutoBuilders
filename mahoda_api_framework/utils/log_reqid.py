import logging.config
import utils.reqid

LOG_CONFIG = {
    'version': 1,
    'filters': {
        'request_id': {
            '()': 'utils.reqid.RequestIdFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(request_id)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
        'app': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
    }
}

FILE_LOG_CONFIG = {
    'version': 1,
    'filters': {
        'request_id': {
            '()': 'utils.reqid.RequestIdFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(request_id)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':'pmts_app.log',
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'standard',
            'maxBytes': 5600,
            'backupCount': 5
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level':'DEBUG',
        },
        'app': {
            'handlers': ['file'],
            'level':'DEBUG',
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)
