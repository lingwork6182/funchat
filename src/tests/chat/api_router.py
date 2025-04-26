# -*- coding:utf-8 -*-
from fastapi import FastAPI

from src.tests.chat.chat import chat

app = FastAPI(description="funchat web api server")

app.post("/api/chat",
         tags=["chat"],
         summary="大模型对话交互接口")(chat)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='192.168.1.19', port=8000)