# -*- coding:utf-8 -*-
from typing import Optional

from fastapi import Body, HTTPException
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain_core.prompts import PromptTemplate
from loguru import logger


def chat(query: str = Body("", description="用户提问"),
         model_name: str = Body("chatglm3-6b", description="基座模型的名称"),
         temperature: float = Body(0.8, description="大模型参数：采样温度", ge=0.0, le=2.0),
         max_tokens: Optional[int] = Body(None, description="大模型参数：最大输入Token限制")
         ):
    logger.info("Received query: {}", query)
    logger.info("Model name: {}", model_name)
    logger.info("Temperature: {}", temperature)
    logger.info("Max tokens: {}", max_tokens)


    try:
        tempfile = """{query}"""
        prompt = PromptTemplate.from_template(tempfile)
        endpoint_url = "http://192.168.1.100:9001/v1/chat/completions"

        llm = ChatGLM3(endpoint_url=endpoint_url,
                       model_name=model_name,
                       temperature=temperature,
                       max_tokens=max_tokens)

        llm_chain = prompt | llm
        response = llm_chain.invoke(query)

        if response is None:
            raise ValueError("Received null response from llm")

        return {"llm response": response}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error" + str(e))
