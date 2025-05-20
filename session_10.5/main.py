from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from LatencyHandler import LatencyHandler

llm = ChatOllama(model='llama3.2:3b',callbacks=[LatencyHandler()])

prompt = ChatPromptTemplate.from_messages(
    [ ("ai","you're a helpful assistant who remebers conversations"),
      ("ai","your name is 'Dan'"),
      ("ai","you're being used for testing purpose"),
      ("ai","you are talking to a user"),
      ("ai","your favorite color is 'blue'"),
      ("ai","your favorite food is 'pizza'"),
      ("ai","your favorite movie is 'Inception'"),
      ("ai","your favorite book is 'The Alchemist'"),
      ("ai","your favorite song is 'Bohemian Rhapsody'"),
      ("ai","your favorite sport is 'soccer'"),  
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
        
prompts = [
    "Hello, how are you?",
    "What is your name?",
    "What are you doing?",
    "What is your purpose?",
    "What is your favorite color?",
    "What is your favorite food?",
    "What is your favorite movie?",
    "What is your favorite book?",
    "What is your favorite song?",
]
    
session_id = "session_1"
    
for prompt in prompts:
    response = chat_with_memory(prompt, session_id)
    print(f"User: {prompt}")
    print(f"Assistant: {response}")
    print("-" * 50)