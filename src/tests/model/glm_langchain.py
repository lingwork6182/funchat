# -*- coding:utf-8 -*-

from langchain.chains.llm import LLMChain
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

template = """{question}"""
prompt = PromptTemplate.from_template(template)
endpoint_url = "http://192.168.1.100:9001/v1/chat/completions"


messages = [
    AIMessage(content="我将从云南到贵州来旅游，出行前希望了解贵州"),
    AIMessage(content="欢迎咨询我任何问题")
]

llm = ChatGLM3(
    endpoint_url=endpoint_url,
    max_tokens=80000,
    prefix_messages=messages,
    top_p=0.5,
)

llm_chain = prompt | llm
question = "贵州西江千户苗寨怎么样？ 计划2天时间，如何规划旅游攻略"

if __name__ == '__main__':
    reponse = llm_chain.invoke(question)
    print(reponse)