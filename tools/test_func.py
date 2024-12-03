import sys

from celery import Celery
import subprocess
import os
from pathlib import Path
# from MsgSender.feishu_msg import send_feishu_info



project_path = Path(__file__).resolve().parent.parent.parent  # 此脚本的运行"绝对"路径
print(project_path)
SCRIPT_PATH = f'{project_path}/sztu_IS/docker-compose.yml'
repo_path = f'{project_path}/sztu_IS'

# 定义 Git 命令
commands = [
    ["docker-compose", "-f", SCRIPT_PATH, "stop", "ali_prod"],

    # ["git", "fetch", "origin"],
    # ["git", "checkout", "-b", "total_celery", "origin/total_celery"],
    # ["git", "checkout", "total_celery"],
    # ["git", "pull", "origin", "total_celery"],

    ["git", "pull"],
    ["git", "branch"],

    # ["docker", "build", "-t", "sztu_is", "."],
    ["docker-compose", "-f", SCRIPT_PATH, "up", "--build", "-d", "ali_prod"],
]


# !!!!每次启动时重新构建
# docker-compose up --build run_web


class LOGGING:
    @staticmethod
    def info(message):
        print(message)

    @staticmethod
    def error(message):
        print(message)

def auto_deploy(a):
    LOGGING.info(str(a))
    LOGGING.info("Hello World!")
    # 使用subprocess.run执行Shell脚本
    try:
        # 执行Shell命令
        # SCRIPT_PATH = "start_deploy.sh"
        # result = subprocess.run(["bash", SCRIPT_PATH], capture_output=True, text=True)
        total_res = ""

        for command in commands:
            if "git" in command or "docker" in command:
                result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)
            else:
                result = subprocess.run(command, capture_output=True, text=True)

            # 输出脚本的标准输出
            total_res += f"Standard Output:{result.stdout}\n"
            if result.stderr:
                total_res += f"Standard Error:{result.stderr}\n"
            total_res += f"Return Code:{result.returncode}\n"
        LOGGING.info(total_res)

        # send_feishu_info("部署结果", total_res)

        return total_res

    except Exception as e:
        LOGGING.error(f"An error occurred: {e}")
        return e


if __name__ == "__main__":
    auto_deploy("single")