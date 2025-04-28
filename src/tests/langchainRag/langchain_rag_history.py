# -*- coding:utf-8 -*-
"""
@NAME: langchain_rag_history.py
@Auth: dabin
@Date: 2025/4/28
"""
import os

import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from zhipuai import ZhipuAI

"""
Step 1. 构建一个能够利用历史消息和最新的用户问题的子链
"""
"""
为了使应用程序能够处理涉及先前交互的问题， 需要先建立一个流程（称为子链），
该子链旨在每当引用过去的讨论时重新表述问题，具体来看：
- 在提示结构中合并了一个名为“chat_history”的变量，它充当历史消息的占位符。通过使用“chat_history”输入键，我们可以将以前的消息列表无缝地注入到提示中。
- 这些消息战略性地放置在系统响应之后和用户提出的最新问题之前，以确保上下文得到维护。
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

""" 
Step 2. 创建提示模板来构建模型的交互
"""
"""该模板包括带有说明的系统消息、聊天历史记录的占位符 ( MessagesPlaceholder ) 以及由 {input} 标记的最新用户问题。"""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ]
)

"""
Step 3. 初始化模型, 该行初始化与 智谱 的 GLM - 4  模型进行连接，将其设置为处理和生成响应。
"""
chat = ChatZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"), model="glm-4", temperature=0.8)

"""
Step 5. 使用加载器创建一个WebBaseLoader，用于网络加载数据
"""

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header"),
        ),
    )
)

docs = loader.load()
print(f"docs: {docs}")

"""
Step 6. 使用 RecursiveCharacterTextSplitter 将内容分割成更小的块，这有助于通过将长文本分解为可管理的大小并有一些重叠来保留上下文来管理长文本。
"""
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

"""
Step 7. Chroma 使用 GLM 4 的 Embedding 模型 提供的嵌入从这些块创建向量存储，从而促进高效检索。
"""
class EmbeddingGenerator:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = self.client.embeddings.create(model=self.model_name, input=text)
            if hasattr(response, 'data') and response.data:
                embeddings.append(response.data[0].embedding)
            else:
                # 如果获取嵌入失败，返回一个零向量
                embeddings.append([0] * 1024)  # 假设嵌入向量维度为 1024
        return embeddings

    def embed_query(self, query):
        # 使用相同的处理逻辑，只是这次只为单个查询处理
        response = self.client.embeddings.create(model=self.model_name, input=query)
        if hasattr(response, 'data') and response.data:
            return response.data[0].embedding
        return [0] * 1024  # 如果获取嵌入失败，返回零向量


# 创建嵌入生成器实例
embedding_generator = EmbeddingGenerator(model_name="embedding-2")

# 文本列表
texts = [content for document in splits for split_type, content in document if split_type == 'page_content']

"""
Step 8. 创建 Chroma VectorStore
"""
chroma_store = Chroma(
    collection_name="example_collection",
    embedding_function=embedding_generator,  # 使用定义的嵌入生成器实例
    create_collection_if_not_exists=True
)

# 添加文本到 Chroma VectorStore
IDs = chroma_store.add_texts(texts=texts)

"""
Step 9. 使用 Chroma VectorStore 创建检索器
"""
retriever = chroma_store.as_retriever()

"""
Step 10. 设置历史信息感知检索器：
create_history_aware_retriever 函数旨在接受输入和“chat_history”的键，用于创建集成聊天历史记录以进行上下文感知处理的检索器。
官方文档：https://python.langchain.com/v0.1/docs/modules/chains/
"""
from langchain.chains import create_history_aware_retriever, history_aware_retriever

history_retriever = create_history_aware_retriever(chat, retriever, contextualize_q_prompt)

# 至此，子链构建结束

"""
Step 11. 构建提示
"""
prompt = hub.pull("rlm/rag-prompt")


# 自定义函数 format_docs 用于适当地格式化这些片段。
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


"""
Step 12. 定义 QA 系统的提示模板，指定系统应如何根据检索到的上下文响应输入。
该字符串设置语言模型的指令，指示它使用提供的上下文来简洁地回答问题。如果答案未知，则指示模型明确说明这一点。
"""

qa_system_prompt = """You are an assistant for question-answering tasks. \  
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 此函数用于创建一个将文档处理与其他流程相结合的链，通常涉及文档检索和在问答等任务中的使用。
from langchain.chains.combine_documents import create_stuff_documents_chain

"""
Step 13 构建问答链：question_answer_chain 是使用 create_stuff_documents_chain 函数创建的，该函数利用语言模型 ( llm ) 和定义的提示 ( qa_prompt )。
官方文档链接：https://python.langchain.com/v0.1/docs/modules/chains/
"""
question_answer_chain = create_stuff_documents_chain(chat, qa_prompt)

# 此函数用于创建将检索功能与处理函数或模型集成的链。
from langchain.chains import create_retrieval_chain

# Step 14. 组装 RAG 链条：该链代表完整的工作流程，其中历史感知检索器首先处理查询以合并任何相关的历史上下文，然后由 question_answer_chain 处理处理后的查询以生成最终答案。
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

"""
Step 14  对话测试
"""
chat_history = []
question = "what is Task Decomposition?"
ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})

chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])

second_question = "what are common ways of dong it?"
ai_msg_2 = rag_chain.invoke({"input": second_question, "chat_history": chat_history})

"""
Step 15. 此命令指示 vectorstore 删除其保存的整个数据集合。这里的集合是指所有文档（文本片段）及其相应的已被索引并存储在向量存储中的向量表示的集合。
"""
chroma_store.delete_collection()
