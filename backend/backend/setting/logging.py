LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatting': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StremHandler',
            'formatter': 'stamdard',
            'filter': [],
        },
    },
    'loggers': {
        'logger_name': {
            'level': 'WARNING',
            'propagate': True,
        } for logger_name in ('django', 'django.request', 'django.db.backends', 'django.templat', 'core')
    },
    'root': {
        'Level': 'DEBUG',
        'handelers': ['console'],
    }
}
