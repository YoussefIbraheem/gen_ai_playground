from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage , AIMessage


llm = ChatOllama(model='llama3.2:3b')

chat_history = []

MODEL_PROMPT = "You're a senior SWE who does mentoring as his part-time job"
prompt = ChatPromptTemplate.from_messages([
    ("system",MODEL_PROMPT),
    ("placeholder","{history}"),
    ("human","{input}")
])

chain = prompt | llm

def send_message_to_llm(user_message):
    chat_history.append(HumanMessage(content=user_message))

    llm_response = chain.invoke({'input':user_message,'history':chat_history})
    
    chat_history.append(AIMessage(content=llm_response.content))
    
    return llm_response