# -*- coding:utf-8 -*-
"""
@NAME: langchain_rag_with_Sqllchermy.py
@Auth: dabin
@Date: 2025/4/28
"""
import os

import bs4
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from langchain_community.chat_message_histories import ChatMessageHistory
from torch.distributed.elastic.utils import store
from zhipuai import ZhipuAI


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = 'sessions'
    __table_args__ = {"comment": "聊天会话"}
    id = Column(Integer, primary_key=True)
    sessoin_id = Column(Integer, unique=True, nullable=False)
    messages = relationship('Message', back_populates='session')


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    session = relationship('Session', back_populates='messages')


def get_db():
    """
    创建一个实用程序函数来管理数据库会话。该函数将确保每个数据库会话正确打开和关闭。
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_message(session_id: str, role: str, content: str):
    """
    定义一个函数将各个消息保存到数据库中。该函数检查会话是否存在；如果没有，它就会创建一个。然后它将消息保存到相应的会话中。
    :param session_id:
    :param role:
    :param content:
    :return:
    """
    db = next(get_db(), None)
    try:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            session = Session(sessoin_id=session_id)
            db.add(session)
            db.commit()
            db.refresh(session)

    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()


def load_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    定义一个函数来从数据库加载聊天历史记录。此函数检索与给定会话 ID 关联的所有消息并重建聊天历史记录。
    :param session_id:
    :return:
    """
    db = next(get_db())
    chat_history = ChatMessageHistory()
    try:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            for message in session.messages:
                chat_history.add_message({"role": message.role, "content": message.content})
    except SQLAlchemyError:
        pass
    finally:
        db.close()

    return chat_history


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    更新 get_session_history 函数以从数据库检索会话历史记录，而不是仅使用内存存储。
    :param session_id:
    :return:
    """
    if session_id not in store:
        store[session_id] = load_session_history(session_id)

    return store[session_id]


def save_all_sessions():
    from langchain_core.messages import HumanMessage, AIMessage

    for session_id, chat_history in store.items():
        for message in chat_history.messages:
            if isinstance(message, dict):
                if "role" in message and "content" in message:
                    save_message(session_id, message["role"], message["content"])
                else:
                    print(f"Skipped a message due to missing keys: {message}")
            elif isinstance(message, HumanMessage):
                save_message(session_id, "human", message.content)
            elif isinstance(message, AIMessage):
                save_message(session_id, "ai", message.content)
            else:
                print(f"Skipped a message due to unknown type: {message}")


def invoke_and_save(session_id, input_text):
    """
    修改链式调用函数，同时保存用户问题和AI答案。这确保了每次交互都被记录下来。
    :param session_id:
    :param input_text:
    :return:
    """
    save_message(session_id, "human", input_text)

    result = conversational_rag_chain.invoke(
        {"input": input_text},
        config={"configurable": {"session_id": session_id}},
    )["answer"]

    print(f"invoke_and_save: {result}")
    save_message(session_id, 'ai', result)

    return result


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
                embeddings.append([0] * 1024)

        return embeddings

    def embed_query(self, query):
        response = self.client.embeddings.create(model=self.model_name, input=query)
        if hasattr(response, 'data') and response.data:
            return response.data[0].embedding

        return [0] * 1024


if __name__ == '__main__':
    # Step 1. 定义模型实例
    chat = ChatZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"), model="glm-4", temperature=0.5)
    # Step 2. 定义 SQLite 数据库以及用于存储会话和消息的模型。
    DATABASE_URL = "sqlite:///chat_history.db"
    # Step 3. 创建模型类. 官网：https://docs.sqlalchemy.org/en/20/orm/quickstart.html
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    # Step 4. 构建Session 来管理会话。官方Docs：https://docs.sqlalchemy.org/en/20/orm/session_basics.html
    SessionLocal = sessionmaker(bind=engine)

    # 使用 atexit 模块来注册一个函数 save_all_sessions，这个函数将在Python程序即将正常终止时自动执行。
    # 目的是在程序退出前保存所有会话数据，以确保不会因程序突然终止而丢失数据。
    import atexit
    atexit.register(save_all_sessions)

    #
    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 创建嵌入生成器实例
    embedding_generator = EmbeddingGenerator(model_name="embedding-2")
    # 文本列表
    texts = [content for document in splits for split_type, content in document if split_type == "page_content"]
    # 创建 Chroma VectorStore
    chroma_store = Chroma(
        collection_name="example_collection",
        embedding_function=embedding_generator,
        create_collection_if_not_exists=True
    )
    # 添加文本到 Chroma VectorStore
    IDs = chroma_store.add_texts(texts=texts)
    print(f"Added documents with IDs: {IDs}")
    # 使用 Chroma VectorStore 创建检索器
    retriever = chroma_store.as_retriever()

    #构建系统的链路信息
    # Contextualize question
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        chat, retriever, contextualize_q_prompt
    )

    # Answer question
    qa_system_prompt = """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        Use three sentences maximum and keep the answer concise.\

        {context}"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )

    question_answer_chain = create_stuff_documents_chain(chat, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    #使用基本字典结构管理聊天历史记录
    # Statefully manage chat history ###
    store = {}
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    result = invoke_and_save("abc123", "what is Task Decomposition?")
    print(result)

    chroma_store.delete_collection()
