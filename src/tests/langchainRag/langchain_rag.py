# -*- coding:utf-8 -*-
"""
@NAME: langchain_rag.py
@Auth: dabin
@Date: 2025/4/28
"""
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.document_loaders import WebBaseLoader
import bs4

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from zhipuai import ZhipuAI


"""
在LangChain中使用 GLM-4 实现基于 Chroma 向量数据库的RAG完整过程。
"""

"""
step01、初始化glm4模型
"""
import os
chat = ChatZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"), model="glm-4", temperature=0.8)

"""
step02、使用加载器创建一个WebBaseLoader，用于网络加载数据
"""


loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()
print(f"docs: {docs}")

"""
Step 03. 使用 RecursiveCharacterTextSplitter 将内容分割成更小的块，这有助于通过将长文本分解为可管理的大小并有一些重叠来保留上下文来管理长文本。
"""

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

for doc_index, doc_splits in enumerate(splits):
    print(f"Document {doc_index+1}:") #显示文档号
    for doc_index, split_text in enumerate(doc_splits):
        print(f"Document {doc_index+1}: {split_text[:50]}...")
    print("\n" + "-" * 60 + "\n")
#
# """
# step 4. Chroma 使用 GLM 4 的 Embedding 模型 提供的嵌入从这些块创建向量存储，从而促进高效检索
# """
# class EmbeddingGenerator:
#     def __init__(self, model_name):
#         self.model_name = model_name
#         self.client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))
#
#     def embed_documents(self, texts):
#         embeddings = []
#         for text in texts:
#             response = self.client.embeddings.create(model=self.model_name, input=text)
#             if hasattr(response, 'data') and response.data:
#                 embeddings.append(response.data[0].embedding)
#             else:
#                 embeddings.append([0] * 1024)
#
#         return embeddings
#
#     def embed_query(self, query):
#         response = self.client.embeddings.create(model=self.model_name, query=query)
#         if hasattr(response, 'data') and response.data:
#             return response.data[0].embedding
#         return [0] * 1024
#
# embedding_generator = EmbeddingGenerator(model_name="embedding-2")
#
# #文本列表
# texts = [content for document in splits for split_type, content in document if split_type == "page_content"]
#
# """
# Step 5. 创建 Chroma VectorStore， 并存入向量
# """
# chroma_store = Chroma(collection_name="example_collection",
#                       embedding_function=embedding_generator,
#                       create_collection_if_not_exists=True
#                     )
#
# IDs = chroma_store.add_texts(texts=texts)
# retriever = chroma_store.as_retriever()
# prompt = hub.pull("rlm/rag-prompt")
#
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)
#
# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | chat
#     | StrOutputParser()
# )
#
# rag_res = rag_chain.invoke("what is Task Decomposition?")
# chroma_store.delete_collection()
