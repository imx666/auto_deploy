import os
import hashlib
import hmac
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from MsgSender.apple_msg import send_apple_info

import json
import requests
from celery import Celery

# 导入日志配置
# import logging
import logging.config
from utils.logging_config import Logging_dict

logging.config.dictConfig(Logging_dict)
LOGGING = logging.getLogger("web_fastapi")

# 获取Webhook密钥
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
BARK_AUTH_CODE = os.getenv("BARK_AUTH_CODE")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_CELERY_DB_CICD = os.getenv("REDIS_CELERY_DB_CICD")
broker_url = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB_CICD}'
LOGGING.info(broker_url)
app_worker = Celery('webhook', broker=broker_url, backend=broker_url)

app = FastAPI()


def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")

    try:
        hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
        expected_signature = "sha256=" + hash_object.hexdigest()
    except Exception as e:
        LOGGING.error(e)

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")


@app.post("/webhook")
async def handle_webhook(request: Request):
    payload_body = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256")
    LOGGING.info(signature_header)

    try:
        verify_signature(payload_body, WEBHOOK_SECRET, signature_header)
        # LOGGING.info(666)
        a = send_apple_info("代码仓库推送", "发送自动部署指令", icon="https://iuxwilson.top/images/github.png")
        LOGGING.info(a)
        app_worker.send_task('webhook.auto_deploy', args=[666])

        # 处理有效请求
        return JSONResponse(content={"message": "Webhook received"}, status_code=200)
    except HTTPException as e:
        LOGGING.error(e)
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


if __name__ == "__main__":
    import uvicorn

    # 启动命令
    # uvicorn main:app --host 0.0.0.0 --port 30001
    uvicorn.run(app, host="0.0.0.0", port=30001)
