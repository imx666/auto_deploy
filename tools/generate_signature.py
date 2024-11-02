import hashlib
import hmac
import os
import json

# 读取请求体
with open('payload.json', 'r') as file:
    payload = file.read()

# 你的Webhook密钥
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# 生成签名
hash_object = hmac.new(WEBHOOK_SECRET.encode('utf-8'), msg=payload.encode('utf-8'), digestmod=hashlib.sha256)
signature = "sha256=" + hash_object.hexdigest()

print(f"Generated Signature: {signature}")