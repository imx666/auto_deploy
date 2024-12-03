
import os
import hashlib
import hmac
# import subprocess
from celery import Celery
import os
from dotenv import load_dotenv

from pathlib import Path
project_path = Path(__file__).resolve().parent  # 此脚本的运行"绝对"路径
# project_path = os.getcwd()  # 此脚本的运行的"启动"路径
dotenv_path = os.path.join(project_path, '../.env.dev')  # 指定.env.dev文件的路径
print(project_path)
load_dotenv(dotenv_path)  # 载入环境变量





# 获取Webhook密钥
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
BARK_AUTH_CODE = os.getenv("BARK_AUTH_CODE")


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_CELERY_DB_CICD = os.getenv("REDIS_CELERY_DB_CICD")
broker_url = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB_CICD}'
print(broker_url)
app_worker = Celery('webhook', broker=broker_url, backend=broker_url)

a='12345678'
result = app_worker.send_task('webhook.auto_deploy', args=[a])

# 检查任务是否完成
print(result.ready())
# 获取任务结果
print(result.get())
