from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory


llm = ChatOllama(model='llama3.2:3b')

prompt = ChatPromptTemplate.from_messages(
    [ ("ai","you're a helpful assistant who remebers conversations"),
      ("ai","your name is 'Dan'"),
      ("ai","you're being used for testing purpose"),
      ("placeholder", "{history}"),
      ("human","{input}")])


memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)

chain = RunnableWithMessageHistory(
    prompt | llm ,
    get_session_history=lambda session_id: memory.chat_memory ,
    history_messages_key="history",
    input_messages_key="input"
)


def chat_with_memory(user_input,session_id):
    response = chain.invoke(
        {'input':user_input},
        config= {"configurable":{"session_id":session_id}}
    ).content
    
    return response
        
    
print( chat_with_memory("what's your name?","conv_1") )
print("-----")
print( chat_with_memory("what's your purpose?","conv_1") )