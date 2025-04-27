# -*- coding:utf-8 -*-
"""
@NAME: model_config.py
@Auth: dabin
@Date: 2025/4/27
"""
from pydantic_settings import BaseSettings

class ModelConfig(BaseSettings):
    TEMPERATURE = 0.8
    LLM_MODELS = ["chatglm3-6b", "zhipu-api"]
    #本地模型
    MODEL_PATH = {
        "local_model": {
            "chatglm3-6b": "/opt/llm/chatglm3/ChatGLM3/ZhipuAI/chatglm3-6b"
        },
        "embed_model": {
            "bge-large-zh-v1.5": "/opt/llm/chatglm3/ChatGLM3/AI-ModelScope/bge-large-zh-v1___5"
        }
    }

    #在线模型
    ONLINE_LLM_MODELS = {
        "zhipu-api": {
            "api_key": "",
            "version": "glm-4",
            "provider": "ChatGLMWorker"
        },

        "openai-api": {
            "model_name": "gpt-4o",
            "api_base_url": "https://api.openai.com/v1/",
            "api_key": "",
            "openai_proxy": ""
        }
    }



model_settings = ModelConfig()