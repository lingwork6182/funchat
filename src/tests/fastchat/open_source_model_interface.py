# -*- coding:utf-8 -*-


import openai

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

"""
运行时先按如下顺序启动服务：
python -m fastchat.serve.controller
python -m fastchat.serve.model_worker --model-path /opt/llm/chatglm3/ChatGLM3/ZhipuAI/chatglm3-6b/ --num-gpus 1
python -m fastchat.serve.openai_api_server
"""

def get_ChatOpenAI() -> ChatOpenAI:
    model = ChatOpenAI(
        openai_api_key="EMPTY",
        openai_api_base="http://192.168.1.100:8000/v1/",
        model_name="chatglm3-6b",
    )
    return model


def test_openai_api():
    model = get_ChatOpenAI()
    template = """{question}"""

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model

    print(chain.invoke("请你介绍一下你自己"))

if __name__ == '__main__':
    test_openai_api()