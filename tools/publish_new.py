
import os
import hashlib
import hmac
# import subprocess
from celery import Celery
import os
from dotenv import load_dotenv

# 指定.env.dev文件的路径
dotenv_path = os.path.join(os.getcwd(), '.env.dev')
print(os.getcwd())

load_dotenv(dotenv_path)
print(os.getenv('WEBHOOK_SECRET'))



# 获取Webhook密钥
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
BARK_AUTH_CODE = os.getenv("BARK_AUTH_CODE")


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_CELERY_DB_CICD = os.getenv("REDIS_CELERY_DB_CICD")
broker_url = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB_CICD}'
app_worker = Celery('webhook', broker=broker_url, backend=broker_url)

a='12345678'
app_worker.send_task('webhook.auto_deploy', args=[a])

