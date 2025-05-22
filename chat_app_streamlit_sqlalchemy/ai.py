from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOllama(model="llama3.2:3b")

prompt = ChatPromptTemplate.from_messages([
        ("ai", "You are a smart assistant named 'Dan'"),
        ("placeholder", "{history}"),
        ("human", "{input}"),
    ])

chain = prompt | llm


def get_chain_w_history(messages):
    return RunnableWithMessageHistory(
        chain, lambda session_id: messages, history_messages_key="chat_hitory"
    )
