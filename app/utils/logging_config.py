def logging_config(filename):
    log_dir = os.path.join(BASE_DIR, "logs")
    # log_path = log_dir + ("/%s.log" % filename)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    return dict(
        {
            "class": "utils.log.InterceptTimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, f"logs/{filename}/{filename}.log"),
            "when": "D",
            "encoding": "utf-8",
            "formatter": "standard",
            "backupCount": 30,
            "interval": 1,
        },
    )


import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)

Logging_dict = {
    "version": 1,
    "disable_existing_loggers": True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    "handlers": {
        "web_fastapi": logging_config("web_fastapi"),
        "celery_worker_cicd": logging_config("celery_worker_cicd"),
    },
    "loggers": {
        "web_fastapi": {
            "handlers": ["web_fastapi"],
            "level": "DEBUG",
            "propagate": False,
        },
        "celery_worker_cicd": {
            "handlers": ["celery_worker_cicd"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
