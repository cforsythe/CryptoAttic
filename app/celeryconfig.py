from celery.schedules import crontab

CELERY_IMPORTS = ('tasks.worker')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'get_coin_list': {
        'task': 'tasks.worker.get_coin_list',
        'schedule': crontab(hour="7"),
    },
    'generate_calls': {
        'task': 'tasks.worker.generate_calls',
        'schedule': crontab(hour="7", minute="1") 
    },
    'get_coin_info': {
        'task': 'tasks.worker.get_coin_info',
        'schedule': 5.0
        }
}
