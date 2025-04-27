# -*- coding:utf-8 -*-
"""
@NAME: open_source_model_interface.py
@Auth: dabin
@Date: 2025/4/27
"""
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


def get_ChatOpenAI()->ChatOpenAI:
    model = ChatOpenAI(
        openai_api_key = "",
        openai_api_base = "http://192.168.1.100:8000/v1/",
        model_name = "chatglm3-6b"
    )

    return model


def test_openai_api():
    model = get_ChatOpenAI()
    template = """{question}"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    print(chain.invoke("请你介绍下你自己"))

if __name__ == '__main__':
    test_openai_api()