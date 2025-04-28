# -*- coding:utf-8 -*-
"""
@NAME: startupdemo.py
@Auth: dabin
@Date: 2025/4/28
"""
import sys
import uuid

from fastchat.serve.controller import app as controller_app, Controller
from fastchat.serve.model_worker import app as worker_app, ModelWorker
from fastchat.serve.openai_api_server import app as openai_server_app, app_settings, CORSMiddleware

import uvicorn

def start_main_server():
    #1、创建controller
    controller = Controller(dispatch_method="shortest_queue")
    sys.modules["fastchat.serve.controller"] = controller
    controller_app.title = "Fast Chat Controller"
    controller_app._controller = controller
    print("Fast Chat Controller Started1")
    uvicorn.run(controller_app, host="192.168.1.100", port=20001)
    print("Fast Chat Controller Started2")

    #2、创建Model Worker
    work_id = str(uuid.uuid4())[:8]

    worker = ModelWorker(
        work_id=work_id,
        controller_address="192.168.1.100:20001",
        worker_addr="192.168.1.100:20002",
        limit_worker_concurrency=5,
        no_register=False,
        model_path="/opt/llm/chatglm3/ChatGLM3/ZhipuAI/chatglm3-6b",
        num_gpus=1,
        model_name="chatglm3-6b",
        device="cuda",
        max_gpu_memory="16GiB"
    )
    worker_app.title = "Fast Chat Worker Server"
    worker_app._worker = worker
    uvicorn.run(worker_app, host="192.168.1.100", port=20002)



    #创建OpenAI API Server
    openai_server_app.title = "Fast Chat Open AI Server"
    openai_server_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app_settings.controller_address = "192.168.1.100:20001"
    app_settings.api_keys = []
    uvicorn.run(openai_server_app, host="192.168.1.100", port=8000)



if __name__ == '__main__':
    start_main_server()