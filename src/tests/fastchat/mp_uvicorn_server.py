# -*- coding:utf-8 -*-
import sys
import uuid
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI
from fastchat.serve.controller import Controller
from fastchat.serve.model_worker import ModelWorker
from fastchat.serve.openai_api_server import app_settings
from starlette.middleware.cors import CORSMiddleware

controller_app = FastAPI(title="FastChat Controller Service")
worker_app = FastAPI(title="FastChat Worker Service")
api_app = FastAPI(title="FastChat OpenAI API Service")


def start_controller():
    controller = Controller(dispatch_method="shortest_queue")
    sys.modules["fastchat.serve.controller"].controller = controller
    controller_app.title = "Controller"
    controller_app._controller = controller
    uvicorn.run(controller_app, host="192.168.1.100", port=20001)

def start_model_worker():
    work_id = str(uuid.uuid4())[:8]
    worker = ModelWorker(
        controller_addr="http://192.168.1.100:20001",
        worker_addr="http://192.168.1.100:20002",
        worker_id=work_id,
        no_register=False,
        limit_worker_concurrency=5,
        model_path="",
        num_gpus=4,
        device="cuda",
        model_names=["chatglm3-6b"],
        max_gpu_memory="16GiB"
    )
    worker_app.title = f"LLM Server"
    worker_app._worker = worker
    uvicorn.run(worker_app, host="192.168.1.100", port=20002)

def start_openai_api_server():
    api_app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,  # 允许前端请求携带认证信息（如 cookies
        allow_origins=["*"],  # 允许所有域名的请求，星号表示不限制任何域。
        allow_methods=["*"],  # 允许所有的 HTTP 方法。
        allow_headers=["*"],  # 允许所有的 HTTP 头
    )
    app_settings.controller_address = "http://192.168.1.100:20001"
    app_settings.api_keys = []
    api_app.title = "FastChat OpenAI API Server"
    uvicorn.run(api_app, host="192.168.1.100", port=8000)

def start_service_mp():
    #创建进程
    controller_process = Process(target=start_controller)
    worker_process = Process(target=start_model_worker)
    api_server_process = Process(target=start_openai_api_server)

    #启动进程
    controller_process.start()
    worker_process.start()
    api_server_process.start()

    #等待所有进程完成
    controller_process.join()
    worker_process.join()
    api_server_process.join()



if __name__ == '__main__':
    start_service_mp()





























